print("Script started!")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import time
from helpers import notify, wait_for_login, auto_login, wait_until_signup_time, fill_form
from settings import (
    STUDENT_NUMBER,
    FULL_NAME,
    EMAIL,
    CELL,
    EMERGENCY,
    COMMENTS,
    UCT_USERNAME,
    UCT_PASSWORD,
    SIGNUP_TIME,
    NO_X,
    NO_Y,
    PAGE_URL,
    require_runtime_settings,
)

def run():
    require_runtime_settings()
    print("Starting Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)

    try:
        # Open Amathuba
        print("Opening Amathuba...")
        driver.get("https://amathuba.uct.ac.za")
        time.sleep(1)

        # Auto-login
        auto_login(driver, wait, UCT_USERNAME, UCT_PASSWORD)

        # Wait until logged in
        wait_for_login(driver)
        time.sleep(1)

        # Navigate to signup page
        print("Navigating to Event Signups...")
        driver.get(PAGE_URL)
        time.sleep(2)

        notify("MSC Signup", "Page loaded! You have 15 seconds to select your event and click Student Number field!")

        print()
        print("="*50)
        print("PAGE IS READY!")
        print("="*50)
        print("You have 15 seconds to:")
        print("  1. Select the event you want")
        print("  2. Click the Student Number field")
        print()
        for i in range(15, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("Filling now!")

        # Fill form
        fill_form(STUDENT_NUMBER, FULL_NAME, EMAIL, CELL, EMERGENCY, COMMENTS, NO_X, NO_Y)

        # Wait until exact signup time then submit
        wait_until_signup_time(SIGNUP_TIME)

        print("Submitting!")
        time.sleep(1)
        pyautogui.press('enter')

        time.sleep(2)
        notify("MSC Signup", "Form submitted! Check browser to confirm.")

        print("="*50)
        print("DONE! Check browser to confirm.")
        print("="*50)
        print("Browser will close automatically in 30 seconds...")
        for i in range(15, 0, -5):
            print(f"Closing in {i} seconds...")
            time.sleep(5)
        print("Closing browser!")

    except Exception as e:
        print(f"\nERROR: {e}")
        notify("MSC Signup Error", str(e))
    finally:
        time.sleep(1)
        driver.quit()

try:
    run()
except Exception as e:
    import traceback
    traceback.print_exc()
    notify("MSC Signup Crashed", str(e))
    input("Press Enter to close...")