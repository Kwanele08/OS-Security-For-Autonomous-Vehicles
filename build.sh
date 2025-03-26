#!/bin/bash

# Start the receiver in the background
python3 receiver.py &
receiver_pid=$!

# Wait a short time for the receiver to start
sleep 0.1

# Start the sender
python3 sender.py

# Run the sniffer in the background
python3 sniffer.py &
sniffer_pid=$!

# Wait for the sender to finish, you might need to adjust this sleep time
sleep 0.1

# Clean up the receiver process
kill $receiver_pid

kill $sniffer_pid

# Unlink (delete) the message queue (IMPORTANT!)
# This is necessary to remove the queue after it's no longer needed.
#rm /dev/mqueue/"$(cat common.py | grep "QUEUE_NAME" | cut -d '"' -f 2)" #Not needed with posix_ipc
python3 -c "import posix_ipc, common; posix_ipc.unlink_message_queue('/' + common.QUEUE_NAME)"

# Print exit code in case the script execution fails
exit $?