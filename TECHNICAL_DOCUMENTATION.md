# DomusOS Technical Documentation

## 1. System overview
DomusOS is a local smart-home management demonstration. Flask serves the HTML/CSS/JavaScript interface and exposes same-origin JSON endpoints. SQLite stores user accounts and a JSON snapshot of each user's dashboard state.

## 2. Architecture
- **Frontend:** HTML, CSS and JavaScript in `templates/index.html`.
- **Backend:** Python Flask application in `app.py`.
- **Database:** SQLite database created at `instance/domusos.sqlite3`.
- **Authentication:** Password hashing and server-managed session cookies.
- **Communication:** JSON requests to the Flask REST API.

## 3. Main components
| File or component | Responsibility |
|---|---|
| `templates/index.html` | Dashboard, login/sign-up UI, device panels, automation trace, safety panel, energy calculator and activity view |
| `app.py` | Flask routes, input validation, session management and persistence |
| `requirements.txt` | Python dependencies |
| `tests/test_api.py` | Automated API tests |
| `benchmark.py` | Repeatable local API timing utility |

## 4. API reference
| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Backend health check |
| POST | `/api/register` | Validate and create an account |
| POST | `/api/login` | Verify credentials and create a session |
| GET | `/api/me` | Return the current signed-in user |
| POST | `/api/logout` | End the current session |
| GET | `/api/state` | Load the signed-in user's saved dashboard state |
| PUT | `/api/state` | Validate and save the signed-in user's dashboard state |

## 5. Data storage and security
- Passwords are stored as Werkzeug password hashes, not plaintext.
- SQL values are parameterized.
- Email addresses are unique without case sensitivity.
- Session cookies are HTTP-only and use SameSite=Lax.
- Saved state must be a JSON object and is limited to 200 KB.
- The local server binds to `127.0.0.1`.

For persistent or public deployment, configure a stable secret key using `DOMUSOS_SECRET_KEY`. Use HTTPS, CSRF protection, rate limiting, a production WSGI server and secure secret management before making the service accessible beyond the local computer.

## 6. Running automated tests
Install dependencies, then run:

```bash
python -m unittest discover -s tests -v
```

The suite exercises backend health, account registration, validation, duplicate registration, login, authenticated state access and persistence.

## 7. Performance measurement
Run:

```bash
python benchmark.py
```

The script measures API response times on the computer where it is run. Record the actual output from the target machine; performance figures vary by hardware and software environment.

## 8. Known scope limits
Device states, sensor readings, alert events, automation actions and energy values are simulated. No physical appliance, smart-home hub, electricity meter or emergency service is connected.
