# Hydroponics Tower Controller

A Python-based controller for managing a hydroponic tower system, designed to monitor and control environmental parameters for optimal plant growth.

## Features

- Real-time monitoring of environmental parameters
- Automated control of water pumps and lighting
- Data logging and visualization
- Configurable settings via YAML configuration
- Support for various sensors and actuators

## Prerequisites

- Python 3.8+
- Raspberry Pi (32-bit ARM)
- Compatible sensors and actuators

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hydrophonics-tower-controller
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt --no-dependencies
   ```
   
   **Note:** This project uses `--no-dependencies` flag because pyarrow (a dependency) cannot be compiled on 32-bit ARM systems. You'll need to install the dependencies manually if they're not already present.

3. Install any missing dependencies individually if needed:
   ```bash
   pip install pyyaml schedule
   ```

## Configuration

1. Copy the example configuration file and modify it according to your setup:
   ```bash
   cp config.example.yaml config.yaml
   ```

2. Edit `config.yaml` to configure your sensors, actuators, and control parameters.

## Usage

Run the main controller script:
```bash
python main.py
```

## Project Structure

- `main.py` - Main application entry point
- `objects.py` - Core classes and data structures
- `cron.py` - Scheduled tasks and automation
- `config.yaml` - Configuration file
- `requirements.txt` - Project dependencies

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
