#!/usr/bin/with-contenv bashio
source /usr/lib/bashio/bashio.sh

exec > >(tee -a /tmp/addon_debug.log) 2>&1  # Log all output to a file

echo "Starting the add-on"

if [ -f "DOCS.md" ]; then
    echo "DOCS.md found"
else
    echo "DOCS.md not found, exiting"
    exit 1
fi

# Load configuration from options.json using jq
if [ -f /data/options.json ]; then
    ADDRESS=$(jq --raw-output '.address' /data/options.json)
    echo "Address from options.json: $ADDRESS"
else
    echo "options.json not found"
    exit 1
fi

# Retrieve config using bashio
ADDRESS1=$(bashio::config 'address')
echo "Address from bashio: $ADDRESS1"

# Fallback if bashio value is not retrieved
if [ -z "$ADDRESS1" ]; then
    echo "bashio failed to retrieve address, using jq value"
    export ADDRESS1="$ADDRESS"
fi

# Start the Flask application
python main.py
