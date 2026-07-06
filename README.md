# MSC Signup Autofiller 🎿⛷️

An automated signup assistant for UCT's Mountain and Skiing Club (MSC) events hosted on Amathuba. This tool handles the tedious parts of event registration - logging in, filling out forms, and submitting at the exact right moment — so you don't have to frantically type while spots disappear in seconds.

> ⚠️ **Disclaimer:** This is a personal automation tool built for educational purposes and my own convenience. Use responsibly and at your own risk. Respect your club's signup policies and don't abuse automation.

---

## What It Does

- **Auto-login** to UCT's Amathuba portal (with Microsoft Authenticator support)
- **Navigate** to the MSC event signups page
- **Auto-fill** your personal details (student number, name, email, cell, emergency contact, comments)
- **Precisely timed submission** — waits until the exact signup time and submits automatically
- **Windows toast notifications** to keep you updated on progress

---

## Project Structure

| File | Description |
|------|-------------|
| `signup_main.py` | **Current main script** — refactored version using `helpers.py` and `settings.py` for cleaner code |
| `signup_better.py` | Alternative version with some UX improvements (manual event selection before form fill) |
| `signup_original_backup.py` | Original first iteration — fully manual login, simpler flow |
| `helpers.py` | Shared utility functions (login handling, form filling, timing logic, notifications) |
| `settings.py` | Configuration loader — reads from `local_settings.py` or environment variables |

---

## Prerequisites

- **Python 3.8+**
- **Google Chrome** installed
- **Windows** (for toast notifications via `win10toast`)

### Dependencies

```bash
pip install selenium webdriver-manager pyautogui pyperclip win10toast
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/jaswin-codes/msc_signup.git
cd msc_signup
```

### 2. Configure your details

Create a `local_settings.py` file in the project root:

```python
# local_settings.py
STUDENT_NUMBER = "ABC123456"
FULL_NAME = "Your Full Name"
EMAIL = "your.email@myuct.ac.za"
CELL = "+27 12 345 6789"
EMERGENCY = "+27 98 765 4321"
COMMENTS = "Any additional comments for the event"

# UCT Login credentials
UCT_USERNAME = "your.student.number@myuct.ac.za"
UCT_PASSWORD = "your_password"

# Signup time — must be in the future when you run the script
SIGNUP_TIME = "2026-07-15 18:00:00"

# Screen coordinates for the "No" radio button (lifts question)
# You may need to adjust these for your screen resolution
NO_X = 902
NO_Y = 971

# URL of the MSC event signups page on Amathuba
PAGE_URL = "https://amathuba.uct.ac.za/d2l/le/lessons/19864/topics/3194308"
```

> 💡 **Tip:** To find `NO_X` and `NO_Y`, open the signup form, hover over the "No" radio button, and use a tool like Python's `pyautogui.position()` or any screen coordinate finder.

### Alternative: Environment Variables

Instead of `local_settings.py`, you can set environment variables:

```bash
set MSC_STUDENT_NUMBER=ABC123456
set MSC_FULL_NAME=Your Full Name
set MSC_EMAIL=your.email@myuct.ac.za
set MSC_CELL=+27 12 345 6789
set MSC_EMERGENCY=+27 98 765 4321
set MSC_COMMENTS=Your comments
set MSC_UCT_USERNAME=your.student.number@myuct.ac.za
set MSC_UCT_PASSWORD=your_password
set MSC_SIGNUP_TIME=2026-07-15 18:00:00
set MSC_NO_X=902
set MSC_NO_Y=971
set MSC_PAGE_URL=https://amathuba.uct.ac.za/d2l/le/lessons/19864/topics/3194308
```

---

## Usage

### Main Script (`signup_main.py`)

```bash
python signup_main.py
```

**Workflow:**
1. Chrome opens and navigates to Amathuba
2. Script attempts auto-login with your credentials
3. Approve **Microsoft Authenticator** on your phone when prompted
4. Script navigates to the event signups page
5. **You have 15 seconds** to select your desired event and click the **Student Number** field
6. Script auto-fills all form fields
7. Countdown begins to the exact signup time
8. At the precise moment, the form is submitted automatically
9. Check your browser to confirm successful registration!

### Alternative Script (`signup_better.py`)

```bash
python signup_better.py
```

This version lets you **manually select the event first**, then press Enter in the terminal before the 10-second countdown to click the Student Number field begins.

---

## How It Works

1. **Selenium WebDriver** opens Chrome and handles navigation
2. **PyAutoGUI** simulates keyboard input and mouse clicks for form interaction
3. **Pyperclip** ensures reliable pasting of text into form fields
4. **Precise timing loop** polls every 0.5 seconds in the final 10 seconds, then submits exactly at `SIGNUP_TIME`
5. **Windows toast notifications** alert you at key milestones (login approval needed, submitting soon, done!)

---

## Notes & Tips

- **Don't move your mouse** during the form-filling phase — PyAutoGUI needs control
- **Keep the browser window focused** when the countdown hits zero
- The script validates that `SIGNUP_TIME` is in the future before running
- If auto-login fails, you can log in manually within the timeout window
- Adjust `NO_X` / `NO_Y` if your screen resolution changes or the page layout shifts

---

## License

MIT License — see [LICENSE](LICENSE) file.

---

*Built with caffeine and the desperate need to secure ski trip spots before they vanish.* ⛷️
