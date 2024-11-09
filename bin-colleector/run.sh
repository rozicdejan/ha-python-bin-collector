#!/usr/bin/env bashio

# Get config value from Home Assistant
export ADDRESS=$(bashio::config 'address')

# Start the Flask application
python main.py