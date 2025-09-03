# Road Car Traffic Counter / Detection System

This is the main entry point for the project. See `/doc` for architecture, requirements, and task breakdowns.

## Quickstart

1. Create and activate a Python virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the main application (to be implemented):
   ```sh
   python main.py
   ```

## Project Structure
- `main.py` — Application entry point
- `camera.py` — Camera input module
- `detection.py` — YOLOv11 detection module
- `tracking.py` — Counting & tracking module
- `traffic_logging.py` — Data logging module
- `config.py` — Configuration management
- `tests/` — Unit and integration tests
- `doc/` — Documentation and task breakdowns

## Setup Tasks
- [x] Initialize Python project structure
- [x] Set up virtual environment
- [x] Install required packages
- [x] Set up Git repository
- [x] Create initial README and architecture documentation
