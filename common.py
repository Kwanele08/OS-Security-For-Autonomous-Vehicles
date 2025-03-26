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
    """Serializes the message to JSON bytes."""
    return json.dumps(message).encode('utf-8')

def deserialize_message(message_bytes):
    """Deserializes the message from JSON bytes."""
    return json.loads(message_bytes.decode('utf-8'))

# --- Simplified Key Management (HARDCODED KEY) ---
# common.py - Corrected 32-byte key
SHARED_SECRET_KEY = b'12345678901234567890123456789012' # Exactly 32 bytes
# **IMPORTANT**: Hardcoding keys like this is insecure in real systems!
# This is acceptable ONLY for this simulation exercise.

# --- ZeroMQ Communication Address ---
# Using TCP on localhost. Could also use "ipc:///tmp/av_secure_comm.ipc"
# but TCP is often easier in containerized environments.
ZMQ_ADDRESS = "tcp://127.0.0.1:5555"