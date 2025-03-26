#!/bin/bash

echo "Starting receiver in the background..."
# Start the receiver - it will bind and wait
python3 receiver.py &
receiver_pid=$!

# Wait a moment for the receiver to bind the socket
sleep 1

echo "Starting sender..."
# Start the sender - it will connect, send, and exit
python3 sender.py

# Wait for the sender to likely finish sending and the receiver to potentially process
# Adjust sleep if needed, or implement more robust signaling
sleep 1

echo "Stopping receiver process (PID: $receiver_pid)..."
# Terminate the receiver process gracefully (SIGTERM)
# If it doesn't stop, use kill -9 $receiver_pid
kill $receiver_pid
wait $receiver_pid 2>/dev/null # Wait for the process to actually exit, suppress errors

echo "Build script finished."

exit 0