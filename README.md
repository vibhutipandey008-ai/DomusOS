# DomusOS — Smart Home Management Software

DomusOS is a browser-based smart-home dashboard with a Python backend and SQLite database. The existing dashboard interface is retained and served by the Flask application.

## Requirements
- Windows 10 or 11
- Python 3.10 or newer
- Internet connection on first launch to install the Flask dependency

## Quick start on Windows
1. Extract the project ZIP into a regular folder.
2. Double-click `Start_DomusOS.bat`.
3. On the first run, the launcher installs the required Python package.
4. Keep the terminal window open while using the application.
5. Open `http://127.0.0.1:8767` if the browser does not open automatically.
6. Create a user account, then sign in.

## Manual start
Open Command Prompt in this folder and run:

```bash
python -m pip install -r requirements.txt
python app.py
```

Then visit `http://127.0.0.1:8767`.

## Project structure
- `app.py` — Flask server, API routes, validation, authentication and database access.
- `templates/index.html` — DomusOS frontend interface.
- `requirements.txt` — Python package dependencies.
- `tests/test_api.py` — automated backend API tests.
- `benchmark.py` — local API timing utility.
- `USER_MANUAL.md` — instructions for operating the application.
- `TECHNICAL_DOCUMENTATION.md` — architecture, API and data details.
- `TESTING_GUIDE.md` — test procedures and evidence checklist.
- `instance/domusos.sqlite3` — created automatically when the application runs.

## Main features
- User registration, sign-in and sign-out.
- Per-user storage for the dashboard's saved demo state.
- Room and device controls.
- Home scenes and configurable automation rules.
- Simulated sensor readings and safety alerts.
- Energy-use and electricity-cost estimates.
- Activity history and voice/typed command interface.

## Scope and limitations
The interface's device states, sensor readings, alert events, automation actions and energy values are software simulations. The application does not currently control physical appliances, connect to a smart-home hub, measure real electricity use or contact emergency services.

The Flask server binds to `127.0.0.1` and is intended for local demonstration. Before exposing an application publicly, deploy it behind HTTPS with a production WSGI server and add appropriate CSRF protection, rate limiting, secure secret management and operational monitoring.
