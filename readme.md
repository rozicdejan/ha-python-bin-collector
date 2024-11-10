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

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/rozicdejan/ha-python-bin-collector).

## License

This project is licensed under the MIT License - see the LICENSE file for details.