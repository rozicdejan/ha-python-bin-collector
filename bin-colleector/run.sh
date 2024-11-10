#!/usr/bin/with-contenv bashio

# Make sure our log directory exists
mkdir -p /logs

# Get configuration from Home Assistant
export OPTIONS_ADDRESS="$(bashio::config 'address')"
export OPTIONS_PORT="$(bashio::config 'port')"
export LOG_FILE="/logs/waste_collection.log"

# Create log file if it doesn't exist
touch "$LOG_FILE"

# Make sure Python can write to the log file
chmod 666 "$LOG_FILE"

bashio::log.info "Starting application on port ${OPTIONS_PORT}"

# Start your Python application with the configured port
# Modify this line according to how your Python script accepts the port number
python3 /usr/src/app/main.py --port "${OPTIONS_PORT}"