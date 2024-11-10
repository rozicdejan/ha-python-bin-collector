#!/usr/bin/with-contenv bashio

# Log all output to a file
exec > >(tee -a /tmp/addon_debug.log) 2>&1

echo "Starting the add-on"

# Check for the presence of DOCS.md
if [ -f "DOCS.md" ]; then
    echo "DOCS.md found"
else
    echo "DOCS.md not found, exiting"
    exit 1
fi

# Retrieve the 'address' configuration using Bashio
if bashio::config.has_value 'address'; then
    ADDRESS=$(bashio::config 'address')
    echo "Address from configuration: $ADDRESS"
else
    echo "Address not set in configuration, exiting"
    exit 1
fi

# Start the Flask application
python main.py
