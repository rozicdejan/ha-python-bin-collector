#!/usr/bin/env bashio

if [ -f "DOCS.md" ]; then
    echo "DOCS.md found"
else
    echo "DOCS.md not found"
    exit 1
fi


# Load configuration from config.json
ADDRESS=$(jq --raw-output '.address' /data/options.json)


# Get config value from Home Assistant
#export ADDRESS=$(bashio::config 'ADDRESS')

# Start the Flask application
python main.py