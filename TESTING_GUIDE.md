# DomusOS Testing Guide

This guide describes how to verify the main application features and record genuine test evidence.

## 1. Automated backend tests
From the project folder, run:

```bash
python -m unittest discover -s tests -v
```

Expected coverage includes:
- Backend health response.
- Valid account registration.
- Invalid registration input.
- Duplicate email handling.
- Successful and unsuccessful login.
- Rejection of signed-out access to protected state.
- Saving and reloading a signed-in user's dashboard state.
- Oversized state payload handling.

Save the actual terminal output as test evidence. Do not mark a test as passed unless it has been run.

## 2. Manual application checks
| Area | Procedure | Expected result |
|---|---|---|
| Registration | Create an account with valid details | Account is created and the user can enter the dashboard |
| Input validation | Submit missing or invalid registration details | A clear validation message appears |
| Duplicate account | Register again with the same email | Duplicate registration is rejected |
| Login | Sign in with the correct password | Dashboard opens |
| Incorrect login | Enter an incorrect password | Access is denied with a clear message |
| Sign out | Use the profile sign-out control | User returns to the sign-in screen |
| State persistence | Change dashboard state, sign out and sign back in | Saved state for that account is restored |
| Device controls | Operate the room/device controls | Displayed simulated state changes |
| Automation | Change simulated sensor values | Matching automation trace and simulated action are displayed |
| Safety panel | Trigger a sensor test | A simulated alert is displayed |
| Energy calculator | Change tariff and usage inputs | Updated estimate is displayed |
| Activity history | Perform actions and open activity history | Events are listed; clear action clears the displayed history |
| Voice interface | Allow microphone access and speak a supported command | Recognized command is displayed and processed, where browser speech recognition is supported |

## 3. Performance measurement
Run:

```bash
python benchmark.py
```

Record the measured output, date, computer specifications and Python version. Results are specific to the test environment.

## 4. Evidence checklist
For each manual test, record:
- Test name and date.
- Steps performed.
- Expected result.
- Actual result.
- Pass or fail.
- Screenshot or terminal output.

## 5. Scope note
Device operations, sensor values, safety alerts, automations and energy estimates are simulated application behaviour. A successful interface test does not demonstrate operation of physical smart-home hardware.
