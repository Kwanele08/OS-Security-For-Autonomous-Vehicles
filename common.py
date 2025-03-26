# common.py
import json
import os

def create_message(sender_id, data):
    """Creates a message dictionary."""
    return {
        'sender': sender_id,
        'data': data,
        'mac': None  # Placeholder for the MAC
    }

def serialize_message(message):
    """Serializes the message to JSON."""
    return json.dumps(message).encode('utf-8')

def deserialize_message(message_bytes):
    """Deserializes the message from JSON."""
    return json.loads(message_bytes.decode('utf-8'))

# --- Simplified Key Management (HARDCODED KEY) ---
# **IMPORTANT**: This is highly insecure for real-world use!
# For a real system, use a proper key exchange/management protocol.
SHARED_SECRET_KEY = os.urandom(32)  # 32 bytes (256 bits) for AES-256
# --- End of Simplified Key Management ---

# --- Message Queue Name ---
QUEUE_NAME = "av_secure_queue"