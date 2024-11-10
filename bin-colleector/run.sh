#!/usr/bin/with-contenv bashio

# Make sure our log directory exists
mkdir -p /logs

# Export configuration from Home Assistant
export OPTIONS_ADDRESS="$(bashio::config 'address')"
export LOG_FILE="/logs/waste_collection.log"

# Create log file if it doesn't exist
touch "$LOG_FILE"

# Make sure Python can write to the log file
chmod 666 "$LOG_FILE"

# Start your Python application
# Replace 'app.py' with your actual Python script name
python3 /usr/src/app/main.py