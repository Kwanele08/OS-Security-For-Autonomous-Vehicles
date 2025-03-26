# sender.py
import posix_ipc  # Import the posix_ipc library
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import common
import os

# ... (rest of your encrypt_data and generate_mac functions remain the same) ...

def send_message(queue_name, sender_id, data):
    """Encrypts, authenticates, and sends a message via POSIX MQ."""
    message = common.create_message(sender_id, data)
    serialized_data = common.serialize_message(message['data'])
    encrypted_data = encrypt_data(serialized_data, common.SHARED_SECRET_KEY)
    mac = generate_mac(encrypted_data, common.SHARED_SECRET_KEY)
    message['mac'] = mac.hex()
    final_message = common.create_message(sender_id, encrypted_data.hex())
    final_message['mac'] = mac.hex()

    try:
        # Open the message queue (create it if it doesn't exist)
        mq = posix_ipc.MessageQueue("/" + queue_name, posix_ipc.O_CREAT, mode=0o600)
        mq.send(common.serialize_message(final_message))  # Use mq.send()
        mq.close()
        print(f"Sent message to queue: /{queue_name}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
     try: #Check if the queue already exists and remove if necessary
         posix_ipc.unlink_message_queue("/" + common.QUEUE_NAME)
     except posix_ipc.ExistentialError:
         pass
     send_message(common.QUEUE_NAME, "perception_module", {"distance": 2.5, "object": "car", "speed": 15.0})