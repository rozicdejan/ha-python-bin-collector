import os
import json
import time
import logging
import threading
import requests
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from threading import Lock
from flask import Flask, jsonify, render_template, Response

# Constants
URL = "https://www.simbio.si/sl/moj-dan-odvoza-odpadkov"
RETRY_COUNT = 3
RETRY_DELAY = 5  # seconds
REQUEST_TIMEOUT = 10  # seconds
UPDATE_INTERVAL = 15 * 60  # 15 minutes in seconds

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Enable proper Unicode handling in JSON responses

# Configure logging
logging.basicConfig(
    format='[BIN-COLLECTOR] %(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'  # Enable UTF-8 encoding for logs
)
logger = logging.getLogger(__name__)

@dataclass
class WasteSchedule:
    id: str
    name: str
    query: str
    city: str
    next_mko: str
    next_emb: str
    next_bio: str

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
    address = os.getenv("ADDRESS")
    if not address:
        address = "ZAČRET 69, LJUBEČNA"
        logger.info(f"No ADDRESS environment variable set, using default: {address}")
    return address

def fetch_data() -> bool:
    address = get_address()
    # Ensure the address is properly encoded for the POST request
    encoded_address = address.encode('utf-8').decode('utf-8')
    payload = f"action=simbioOdvozOdpadkov&query={encoded_address}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    }

    try:
        response = requests.post(URL, data=payload.encode('utf-8'), headers=headers, timeout=REQUEST_TIMEOUT)
        response.encoding = 'utf-8'  # Ensure response is interpreted as UTF-8
        response.raise_for_status()
        schedules = response.json()

        if not schedules:
            raise ValueError("No data received in the response")

        first_schedule = schedules[0]

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
        logger.error(f"Error fetching data: {str(e)}")
        return False

def fetch_data_with_retry() -> bool:
    for attempt in range(RETRY_COUNT):
        if fetch_data():
            return True
        logger.warning(f"Attempt {attempt + 1} failed, retrying...")
        time.sleep(RETRY_DELAY)
    
    logger.error("All retry attempts failed")
    return False

def data_updater():
    while True:
        fetch_data_with_retry()
        time.sleep(UPDATE_INTERVAL)

@app.route('/')
def data_handler():
    with waste_data.lock:
        return render_template('template.html', data=waste_data.template)

@app.route('/api/data')
def api_data_handler():
    with waste_data.lock:
        response = jsonify(waste_data.full)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

def main():
    logger.info("Starting bin collector service...")
    
    # Initial data fetch
    if not fetch_data_with_retry():
        logger.error("Initial data fetch failed")
    
    # Start background updater in a separate thread
    updater_thread = threading.Thread(target=data_updater, daemon=True)
    updater_thread.start()
    
    # Start server
    app.run(host='0.0.0.0', port=8081)

if __name__ == '__main__':
    main()
