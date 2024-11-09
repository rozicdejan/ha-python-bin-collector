# Bin Collection Schedule Add-on

## Installation

1. Add the repository to your Home Assistant instance (Settings -> Add-ons -> Add-on Store -> ⋮ -> Repositories):
   ```
   https://github.com/yourusername/ha-bin-collection
   ```

2. Install the "Bin Collection Schedule" add-on

## Configuration

Add-on configuration:

```yaml
address: "your street address"  # Required: Your street address for waste collection schedule
```

## How to use

1. Install the add-on
2. Configure your address in the add-on configuration
3. Start the add-on
4. Access the web interface at `http://your-ha-ip:8081`

The interface will display your waste collection schedule with three categories:
- Mixed waste (Mešani komunalni odpadki)
- Packaging (Embalaža)
- Biological waste (Biološki odpadki)

The schedule automatically updates every 15 minutes.

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/yourusername/ha-bin-collection/issues).