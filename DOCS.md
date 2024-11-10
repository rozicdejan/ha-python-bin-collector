# Bin Collection Schedule - Simbio

## Overview

The Bin Collection Schedule add-on for Home Assistant provides automated waste collection schedule information for residents served by Simbio waste management in Slovenia. It fetches data from Simbio's official website and presents it through both a web interface and an API endpoint.

Current version: **2.0.0**

## Installation

1. In Home Assistant, navigate to **Supervisor** → **Add-on Store**
2. Click the menu icon (⋮) in the top right
3. Select **Repositories**
4. Add `https://github.com/rozicdejan/ha-python-bin-collector`
5. Find "Bin Collection Schedule - Simbio" in the add-on store
6. Click **Install**

## Configuration

### Add-on Configuration

```yaml
address: "POLJSKA POT 6, LJUBEČNA"
port: 8081
```

### Configuration Options

| Option   | Required | Default | Description |
|----------|----------|---------|-------------|
| address  | Yes      | "POLJSKA POT 6, LJUBEČNA" | Your street address for collection schedule |
| port     | No       | 8081    | Port for the web interface |

## System Requirements

### Supported Architectures
- aarch64
- amd64
- armhf
- armv7
- i386

### Startup & Boot
- Startup: `application`
- Boot: `auto`
- Init: `false`

### Network
- Default port: 8081 (TCP)
- WebUI: `http://[HOST]:[PORT:8081]/`

### File System Access
The add-on requires access to:
- SSL
- Config (read/write)
- Additional mapping: `/share/waste_collection/logs:/logs`

## Features

### Web Interface
- Access at `http://[HOST]:[PORT:8081]/`
- Displays next collection dates for:
  - Mixed Municipal Waste
  - Packaging
  - Biological Waste
- Auto-refreshes every 15 minutes

### REST API
- Endpoint: `http://[HOST]:[PORT:8081]/api/data`
- Returns JSON with collection schedules
- Updates automatically every 15 minutes

### Logging
- Logs are stored at path specified by `LOG_FILE` environment variable
- Default log location: `/tmp/waste_collection.log`
- Additional logs in `/share/waste_collection/logs`

## Technical Details

### API Response Format

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

### Service Operation
- Data source: `https://www.simbio.si/sl/moj-dan-odvoza-odpadkov`
- Update interval: 15 minutes
- Automatic retry mechanism (3 attempts)
- UTF-8 encoding support for Slovenian characters

## Troubleshooting

### Common Issues

1. **Add-on Won't Start**
   - Verify the address format
   - Check if the port is available
   - Review the logs

2. **No Data Available**
   - Confirm address is in Simbio's service area
   - Check internet connectivity
   - Review connection logs

3. **Incorrect Schedule**
   - Verify address format matches Simbio's records
   - Ensure address includes house number and city

### Logging
Logs can be accessed through:
1. Home Assistant UI: **Supervisor** → **Bin Collection Schedule** → **Logs**
2. Direct access to `/tmp/waste_collection.log`
3. Additional logs in `/share/waste_collection/logs`

## Integration Examples

### Home Assistant Sensor

```yaml
sensor:
  - platform: rest
    name: next_waste_collection
    resource: http://localhost:8081/api/data
    json_attributes:
      - mko_date
      - emb_date
      - bio_date
    value_template: "{{ value_json.mko_date }}"
```

### Automation Example

```yaml
automation:
  - alias: "Waste Collection Reminder"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: template
        value_template: >
          {% set collection_date = states.sensor.next_waste_collection.attributes.mko_date %}
          {{ collection_date == (now().date() + timedelta(days=1)).isoformat() }}
    action:
      - service: notify.mobile_app
        data:
          message: "Remember to put out the mixed waste bins tomorrow!"
```

## Support

For support:
1. Check the documentation
2. Review GitHub issues
3. Open a new issue with:
   - Add-on version (1.1.95)
   - Home Assistant version
   - Relevant logs
   - Steps to reproduce the problem

## License

This project is licensed under the MIT License. See the LICENSE file in the repository for full details.