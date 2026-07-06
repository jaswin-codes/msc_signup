from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import pyperclip
import time
from datetime import datetime
from settings import (
    STUDENT_NUMBER,
    FULL_NAME,
    EMAIL,
    CELL,
    EMERGENCY,
    COMMENTS,
    SIGNUP_TIME,
    NO_X,
    NO_Y,
    PAGE_URL,
    require_runtime_settings,
)

def paste(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.25)

def wait_until_signup_time():
    target = datetime.strptime(SIGNUP_TIME, "%Y-%m-%d %H:%M:%S")
    print(f"\nForm filled! Waiting until {target} to submit...")
    while True:
        diff = (target - datetime.now()).total_seconds()
        if diff <= 0:
            print("Time reached! Submitting now...")
            break
        elif diff <= 10:
            print(f"{diff:.1f} seconds remaining...")
            time.sleep(0.5)
        else:
            print(f"{int(diff)} seconds remaining...")
            time.sleep(5)

def fill_form():
    print("Filling form...")
    time.sleep(0.3)

    # Student Number (cursor should be here)
    paste(STUDENT_NUMBER)
    pyautogui.press('tab')
    time.sleep(0.3)

    # Name
    paste(FULL_NAME)
    pyautogui.press('tab')
    time.sleep(0.3)

    # Email
    paste(EMAIL)
    pyautogui.press('tab')
    time.sleep(0.3)

    # Cell
    paste(CELL)
    pyautogui.press('tab')
    time.sleep(0.3)

    # Emergency
    paste(EMERGENCY)
    pyautogui.press('tab')
    time.sleep(0.3)

    # Click No for lifts
    print("Selecting No for lifts...")
    pyautogui.click(NO_X, NO_Y)
    time.sleep(0.3)

    # Comments
    pyautogui.press('tab')
    time.sleep(0.3)
    paste(COMMENTS)
    time.sleep(0.3)

    print("All fields filled!")

def run():
    require_runtime_settings()
    print("Starting Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open Amathuba
        print("Opening Amathuba...")
        driver.get("https://amathuba.uct.ac.za")
        time.sleep(3)

        # Manual login
        print("="*50)
        print("Please log in and approve Authenticator.")
        print("You have 60 seconds...")
        print("="*50)
        time.sleep(60)
        print("Continuing...")

        # Go to signup page
        print("Navigating to Event Signups page...")
        driver.get(PAGE_URL)
        time.sleep(2)

        # Instructions
        print()
        print("="*50)
        print("PAGE IS READY!")
        print("="*50)
        print()
        print("1. Select the event you want to sign up for")
        print("2. Come back to this terminal")
        print("3. Press Enter")
        print()
        input("Press Enter once you have selected your event...")

        # Countdown to go back to browser and click Student Number
        print()
        print("You have 10 seconds to click the Student Number field!")
        for i in range(10, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("Go!")

        # Fill the form immediately
        fill_form()

        # Wait until exact signup time
        wait_until_signup_time()

        # Press Enter to submit
        print("Submitting!")
        pyautogui.press('enter')

        print("="*50)
        print("DONE! Check browser to confirm submission.")
        print("="*50)
        time.sleep(5)

    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()

try:
    run()
except Exception as e:
    import traceback
    traceback.print_exc()
    input("Press Enter to close...")