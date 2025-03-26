# sniffer.py
'''
import os
import common
import sys
import posix_ipc

def sniff_message(queue_name):
    """Attempts to read a message from the queue without decryption."""
    try:
        mq = posix_ipc.MessageQueue("/" + queue_name)
        msg_bytes, _ = mq.receive()
        mq.close()

        print("Sniffed raw message bytes:")
        print(msg_bytes)  # Print the raw bytes (will be unreadable)
        # Attempt to deserialize (should fail if no tampering is done)
        try:
            message = common.deserialize_message(msg_bytes)
            print("Deserialized (without decryption):",message)
        except Exception:
            print("Could not deserialize the message")


    except Exception as e:
        print(f"Error sniffing message: {e}")

if __name__ == "__main__":
    sniff_message(common.QUEUE_NAME)'''