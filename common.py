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

# Simplified Key Management (HARDCODED KEY) ---
SHARED_SECRET_KEY = b'12345678901234567890123456789012' 

# ZeroMQ Communication Address ---
ZMQ_ADDRESS = "tcp://127.0.0.1:5555"
