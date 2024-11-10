#!/usr/bin/env bashio
source /usr/lib/bashio/bashio.sh  # Ensure bashio is sourced

if [ -f "DOCS.md" ]; then
    echo "DOCS.md found"
else
    echo "DOCS.md not found"
    exit 1
fi

# Load configuration from config.json using jq
ADDRESS=$(jq --raw-output '.address' /data/options.json)
echo "Address from options.json: $ADDRESS"

# Get config value from Home Assistant using bashio
export ADDRESS1=$(bashio::config 'address')
echo "Address from bashio: $ADDRESS1"

# Fallback if bashio fails
if [ -z "$ADDRESS1" ]; then
    echo "bashio failed to retrieve address, using jq value"
    export ADDRESS1="$ADDRESS"
fi

cat /data/options.json


# Start the Flask application
python main.py
