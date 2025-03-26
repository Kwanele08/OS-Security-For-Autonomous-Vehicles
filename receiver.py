# receiver.py
import posix_ipc  # Import the posix_ipc library
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import common
import os

# ... (rest of your decrypt_data and verify_mac functions remain the same) ...

def receive_message(queue_name):
    """Receives, verifies, and decrypts a message from POSIX MQ."""
    try:
        mq = posix_ipc.MessageQueue("/" + queue_name) # No O_CREAT flag here
        msg_bytes, _ = mq.receive() # Use mq.receive()
        mq.close()

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

    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

if __name__ == "__main__":
    received_data = receive_message(common.QUEUE_NAME)
    if received_data:
        pass