#!/usr/bin/env bashio
source /usr/lib/bashio/bashio.sh

if [ -f "DOCS.md" ]; then
    echo "DOCS.md found"
else
    echo "DOCS.md not found"
    exit 1
fi

# Get config value from Home Assistant
export ADDRESS=$(bashio::config 'ADDRESS')

# Start the Flask application
python main.py