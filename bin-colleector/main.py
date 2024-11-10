import os
import json
import time
import logging
import threading
import requests
import argparse
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from threading import Lock
from flask import Flask, jsonify, render_template, Response

# Set up logging before anything else
LOG_FILE = os.getenv('LOG_FILE', '/logs/waste_collection.log')
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='[BIN-COLLECTOR] %(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console handler
        logging.FileHandler(LOG_FILE, encoding='utf-8')  # File handler
    ]
)

# Get the logger
logger = logging.getLogger(__name__)

# Test logging immediately
logger.info("Starting script initialization...")
logger.info(f"Log file location: {LOG_FILE}")

# Print all environment variables for debugging (be careful with sensitive data)
logger.info("Environment variables:")
for key, value in os.environ.items():
    if 'ADDRESS' in key:  # Only log address-related variables
        logger.info(f"{key}: {value}")

# Constants
URL = "https://www.simbio.si/sl/moj-dan-odvoza-odpadkov"
RETRY_COUNT = 3
RETRY_DELAY = 5
REQUEST_TIMEOUT = 10
UPDATE_INTERVAL = 15 * 60

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Rest of your classes remain the same...
@dataclass
class TemplateData:
    mko_name: str = "Mešani komunalni odpadki"
    mko_date: str = ""
    emb_name: str = "Embalaža"
    emb_date: str = ""
    bio_name: str = "Biološki odpadki"
    bio_date: str = ""

@dataclass
class FullData:
    name: str
    query: str
    city: str
    mko_name: str = "Mešani komunalni odpadki"
    mko_date: str = ""
    emb_name: str = "Embalaža"
    emb_date: str = ""
    bio_name: str = "Biološki odpadki"
    bio_date: str = ""

class WasteData:
    def __init__(self):
        self.lock = Lock()
        self.template = TemplateData()
        self.full = Optional[FullData]

waste_data = WasteData()

def get_address() -> str:
    # Fallback to ADDRESS
    address = os.getenv("ADDRESS")
    if address:
        logger.info(f"Found ADDRESS: {address}")
        return address
    
    address = os.getenv("ADDRESS1")
    if address:
        logger.info(f"Found ADDRESS: {address}")
        return address
    
    # Get address from OPTIONS_ADDRESS first
    address = os.getenv("OPTIONS_ADDRESS")
    if address:
        logger.info(f"Found OPTIONS_ADDRESS: {address}")
        return address
       
    # Default address as last resort
    default_address = "začret 67"
    logger.warning(f"No address found in environment, using default: {default_address}")
    return default_address

def get_port() -> int:
    # Get port from environment variable first (set by Home Assistant)
    port = os.getenv("OPTIONS_PORT")
    if port:
        try:
            return int(port)
        except (TypeError, ValueError):
            logger.warning(f"Invalid port in OPTIONS_PORT: {port}, using default")
    
    # Default port as fallback
    return 8081

def fetch_data() -> bool:
    address = get_address()
    logger.info(f"Attempting to fetch data for address: {address}")
    
    encoded_address = address.encode('utf-8').decode('utf-8')
    payload = f"action=simbioOdvozOdpadkov&query={encoded_address}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    }

    try:
        logger.info(f"Making POST request to {URL}")
        response = requests.post(URL, data=payload.encode('utf-8'), headers=headers, timeout=REQUEST_TIMEOUT)
        response.encoding = 'utf-8'
        response.raise_for_status()
        schedules = response.json()

        if not schedules:
            logger.error("No data received in response")
            raise ValueError("No data received in the response")

        first_schedule = schedules[0]
        logger.info(f"Received data for: {first_schedule['name']} in {first_schedule['city']}")

        with waste_data.lock:
            waste_data.template = TemplateData(
                mko_date=first_schedule['next_mko'],
                emb_date=first_schedule['next_emb'],
                bio_date=first_schedule['next_bio']
            )
            
            waste_data.full = FullData(
                name=first_schedule['name'],
                query=first_schedule['query'],
                city=first_schedule['city'],
                mko_date=first_schedule['next_mko'],
                emb_date=first_schedule['next_emb'],
                bio_date=first_schedule['next_bio']
            )
        
        return True

    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}", exc_info=True)
        return False

def fetch_data_with_retry() -> bool:
    for attempt in range(RETRY_COUNT):
        logger.info(f"Fetch attempt {attempt + 1} of {RETRY_COUNT}")
        if fetch_data():
            return True
        logger.warning(f"Attempt {attempt + 1} failed, retrying...")
        time.sleep(RETRY_DELAY)
    
    logger.error("All retry attempts failed")
    return False

def data_updater():
    while True:
        logger.info("Running scheduled data update")
        fetch_data_with_retry()
        logger.info(f"Sleeping for {UPDATE_INTERVAL} seconds")
        time.sleep(UPDATE_INTERVAL)

@app.route('/')
def data_handler():
    logger.info("Handling web request for /")
    with waste_data.lock:
        return render_template('template.html', data=waste_data.template)

@app.route('/api/data')
def api_data_handler():
    logger.info("Handling API request for /api/data")
    with waste_data.lock:
        response = jsonify(waste_data.full)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

def main():
    logger.info("=== Starting Waste Collection Service ===")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    # Get port number from environment
    port = get_port()
    logger.info(f"Using port: {port}")
    
    # Initial data fetch
    if not fetch_data_with_retry():
        logger.error("Initial data fetch failed")
    else:
        logger.info("Initial data fetch successful")
    
    # Start background updater
    logger.info("Starting background updater thread")
    updater_thread = threading.Thread(target=data_updater, daemon=True)
    updater_thread.start()
    
    # Start Flask server
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()