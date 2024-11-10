# Bin Collection Schedule - Simbio

![Validates with hassfest](https://img.shields.io/badge/hassfest-passing-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<!-- Screenshoot image -->
![Alt Text](https://github.com/rozicdejan/ha-python-bin-collector/blob/main/pictures/ha-screenshoot.png?raw=true)

## About

This Home Assistant add-on displays waste collection schedules for residents served by Simbio waste management in Slovenia. It fetches and displays upcoming collection dates for different types of waste (mixed waste, packaging, and bio waste).

Current version: **2.0.0**

## Features

- Real-time waste collection schedule information
- Supports three waste types:
  - Mixed Municipal Waste (Mešani komunalni odpadki)
  - Packaging (Embalaža)
  - Biological Waste (Biološki odpadki)
- Automatic updates every 15 minutes
- Web interface for easy viewing
- REST API endpoint for integration
- Detailed logging for troubleshooting

## Installation

[![Button Text](https://my.home-assistant.io/badges/supervisor_store.svg)](https://my.home-assistant.io/redirect/supervisor_store/)

1. Navigate to your Home Assistant Supervisor panel
2. Click on the Add-on Store
3. Add this repository URL: `https://github.com/rozicdejan/ha-python-bin-collector`
4. Install the "Bin Collection Schedule - Simbio" add-on

## Configuration

The add-on can be configured via the Home Assistant UI. These options are available:

```yaml
address: "ZAČRET 69, LJUBEČNA"  # Required: Your street address
port: 8081                      # Optional: Web interface port (default: 8081) -enable port!
```

## Supported Architectures

- aarch64
- amd64
- armhf
- armv7
- i386

## Network

The add-on exposes a web interface on port 8081 (configurable). You can access it at:
`http://[HOST]:[PORT:8081]/`

## API Response Example
## REST API Usage

The add-on also provides a REST API endpoint to retrieve the waste collection schedule programmatically. Below are the details of the API response structure:

Endpoint

URL: /api/data

Method: GET

Response Example

The response is returned in JSON format and contains information on upcoming waste collections for the specified address.

```json
{
  "name": "Street Name",
  "query": "entered_address",
  "city": "City Name",
  "mko_name": "Mešani komunalni odpadki",
  "mko_date": "2024-01-01",
  "emb_name": "Embalaža",
  "emb_date": "2024-01-02",
  "bio_name": "Biološki odpadki",
  "bio_date": "2024-01-03"
}
```

## Response Fields Explained

name: The name of the street or location for which the schedule applies.

query: The originally queried address, reflecting the input used to generate the schedule.

city: The city corresponding to the queried address.

mko_name: The type of waste (Mixed Municipal Waste).

mko_date: The next collection date for Mixed Municipal Waste.

emb_name: The type of waste (Packaging).

emb_date: The next collection date for Packaging waste.

bio_name: The type of waste (Biological Waste).

bio_date: The next collection date for Biological Waste.

## Example Usage

To access the waste collection schedule via the REST API, simply make a GET request to:

```json
http://[HOST]:8081/api/data
```

Here is an example of retrieving data using curl:

```json
curl -X GET http://localhost:8081/api/data
```
You should receive a response similar to the example provided above.


## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/rozicdejan/ha-python-bin-collector).

## License

This project is licensed under the MIT License - see the LICENSE file for details.