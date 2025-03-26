# sender.py
import zmq # Import ZeroMQ
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import common
import time
import os

# --- Cryptography Functions (No changes needed) ---
def encrypt_data(data, key):
    """Encrypts the data using AES-256 in CBC mode."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def generate_mac(data, key):
    """Generates an HMAC-SHA256 MAC for the data."""
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    return h.finalize()
# --- End Cryptography Functions ---

def send_message(context, sender_id, data):
    """Encrypts, authenticates, and sends a message via ZeroMQ PUSH socket."""

    # Prepare socket (Connect to the receiver's address)
    socket = context.socket(zmq.PUSH)
    socket.connect(common.ZMQ_ADDRESS)
    print(f"Sender connected to {common.ZMQ_ADDRESS}")

    try:
        # --- Prepare message (Same as before) ---
        message = common.create_message(sender_id, data)
        serialized_data = common.serialize_message(message['data'])
        encrypted_data = encrypt_data(serialized_data, common.SHARED_SECRET_KEY)
        mac = generate_mac(encrypted_data, common.SHARED_SECRET_KEY)
        message['mac'] = mac.hex()
        final_message = common.create_message(sender_id, encrypted_data.hex())
        final_message['mac'] = mac.hex()
        # --- End Prepare message ---

        # Serialize the final message for sending
        message_bytes = common.serialize_message(final_message)

        # Add a small delay to ensure receiver is ready (especially on first run)
        time.sleep(0.5)

        # Send the message bytes via ZeroMQ
        socket.send(message_bytes)
        print(f"Sent message from {sender_id}")

    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        # Clean up the socket
        socket.close()
        print("Sender socket closed.")


if __name__ == "__main__":
    # Create a single ZeroMQ context for the application
    zmq_context = zmq.Context()

    # Example usage:
    send_message(zmq_context, "perception_module", {"distance": 5.8, "object": "pedestrian", "speed": 2.1})

    # Clean up the context
    zmq_context.term()
    print("Sender context terminated.")