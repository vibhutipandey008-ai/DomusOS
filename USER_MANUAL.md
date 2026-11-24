# DomusOS User Manual

## 1. Start the application
1. Extract the project ZIP.
2. Double-click `Start_DomusOS.bat`.
3. Wait while the launcher installs Flask (first run) and starts the server.
4. If the browser does not open automatically, visit `http://127.0.0.1:8767`.
5. Keep the terminal window open while using DomusOS.

## 2. Create an account
1. Select **Sign up**.
2. Enter your name and email address.
3. Choose a password of at least eight characters and confirm it.
4. Submit the form.
5. The account is saved in the local SQLite database on this computer.

## 3. Sign in and sign out
Sign in with the email address and password used during registration. Use **Keep me signed in** if you want the browser session to persist. Use the profile control to sign out.

## 4. Use the dashboard
- **Overview:** view the home summary, scenes, command interface and recent activity.
- **Rooms & devices:** operate the simulated lights, fan, smart plug and curtains, and adjust available controls.
- **Automations:** enable or disable rules and change simulated sensor values to view the execution trace.
- **Safety & alerts:** arm or disarm the demonstration system and trigger simulated sensor events.
- **Energy & cost:** change the tariff, usage hours, billing days and additional load to calculate an estimate.
- **Activity history:** review or clear the activity events shown by the application.

## 5. Voice and typed commands
Voice recognition depends on browser support, microphone permission and the browser's speech service. If voice input is unavailable, use the typed command field.

## 6. Stop the application
Close the DomusOS terminal window or press `Ctrl+C` in that window.

## 7. Troubleshooting
- **Python is not recognized:** install Python 3 and enable its PATH option, then reopen Command Prompt.
- **Dependency installation fails:** check internet access and run `python -m pip install -r requirements.txt` from the project folder.
- **Port 8767 is busy:** close the other local server using that port or change the port consistently in `app.py`, `Start_DomusOS.bat` and this manual.
- **Cannot sign in:** confirm that the account was created in this browser installation and use the same email and password.
- **Microphone does not respond:** check browser microphone permissions and Windows microphone privacy settings.

## 8. Important limitations
DomusOS currently simulates device states, sensor readings, alert events, automation actions and energy estimates. It does not control physical appliances or provide real emergency monitoring.
