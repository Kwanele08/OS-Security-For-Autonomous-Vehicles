# receiver.py
import zmq 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import common
import os

# Cryptography Functions 
def decrypt_data(ciphertext, key):
    """Decrypts the data using AES-256 in CBC mode."""
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

def verify_mac(data, mac, key):
    """Verifies the HMAC-SHA256 MAC."""
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    try:
        h.verify(mac)
        return True
    except InvalidSignature:
        return False
# End Cryptography Functions 

def receive_message(context):
    """Receives, verifies, and decrypts a message from ZeroMQ PULL socket."""

    # Prepare socket (Bind to the address senders will connect to)
    socket = context.socket(zmq.PULL)
    socket.bind(common.ZMQ_ADDRESS)
    print(f"Receiver bound to {common.ZMQ_ADDRESS}, waiting for messages...")

    try:
        # Receive message bytes (this will block until a message arrives)
        msg_bytes = socket.recv()

        # Process message
        message = common.deserialize_message(msg_bytes)
        received_mac = bytes.fromhex(message['mac'])
        received_data = bytes.fromhex(message['data'])

        if not verify_mac(received_data, received_mac, common.SHARED_SECRET_KEY):
            print("ERROR: Message authentication failed! Discarding message.")
            return None

        decrypted_data_bytes = decrypt_data(received_data, common.SHARED_SECRET_KEY)
        decrypted_data = common.deserialize_message(decrypted_data_bytes)

        print(f"Received message from {message['sender']}: {decrypted_data}")
        return decrypted_data
        # End Process message

    except Exception as e:
        print(f"Error receiving message: {e}")
        return None
    finally:
        # Clean up the socket
        socket.close()
        print("Receiver socket closed.")


if __name__ == "__main__":
    # Create a single ZeroMQ context for the application
    zmq_context = zmq.Context()

    # Example usage:
    received_data = receive_message(zmq_context)
    if received_data:
        # Process the received data (e.g., update vehicle state)
        pass

    # Clean up the context
    zmq_context.term()
    print("Receiver context terminated.")
