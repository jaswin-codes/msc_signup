print("Script started!")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    UCT_USERNAME,
    UCT_PASSWORD,
    SIGNUP_TIME,
    NO_X,
    NO_Y,
    PAGE_URL,
    require_runtime_settings,
)

def notify(title, message):
    """Show a Windows popup notification"""
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5, threaded=True)
    except:
        print(f"[NOTIFICATION] {title}: {message}")

def paste(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)

def wait_for_login(driver):
    """Wait until login is complete by checking URL change"""
    print("Waiting for you to log in and approve Authenticator...")
    print("(Will auto-continue once logged in, max 90 seconds)")
    timeout = 90
    start = time.time()
    while time.time() - start < timeout:
        try:
            if "login" not in driver.current_url.lower() and \
               "microsoftonline" not in driver.current_url.lower():
                print("Login detected! Continuing...")
                return True
        except:
            pass
        time.sleep(1)
    notify("MSC Signup", "Login timeout! Please restart the script.")
    raise Exception("Login timed out after 90 seconds")

def auto_login(driver, wait):
    try:
        # Click UCT LOGIN button first
        print("Clicking UCT LOGIN button...")
        uct_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.d2l-button")
        ))
        uct_btn.click()
        time.sleep(2)

        # Enter username
        print("Entering username...")
        username_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='email'], input[name='loginfmt']")
        ))
        username_field.clear()
        username_field.send_keys(UCT_USERNAME)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)

        # Enter password
        print("Entering password...")
        password_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='password']")
        ))
        password_field.clear()
        password_field.send_keys(UCT_PASSWORD)
        time.sleep(0.5)
        pyautogui.press('enter')
        print("Credentials entered! Approve Authenticator on your phone...")
        notify("MSC Signup", "Approve Microsoft Authenticator now!")

    except Exception as e:
        print(f"Auto-login failed ({e}), please log in manually...")
        notify("MSC Signup", "Auto-login failed - please log in manually!")

def wait_until_signup_time():
    target = datetime.strptime(SIGNUP_TIME, "%Y-%m-%d %H:%M:%S")
    print(f"\nForm filled! Waiting until {target} to submit...")
    notified = False
    while True:
        diff = (target - datetime.now()).total_seconds()
        if diff <= 0:
            print("Time reached! Submitting now...")
            break
        elif diff <= 30 and not notified:
            notify("MSC Signup", f"Submitting in {int(diff)} seconds!")
            notified = True
        if diff <= 10:
            print(f"{diff:.1f} seconds remaining...")
            time.sleep(0.5)
        else:
            print(f"{int(diff)} seconds remaining...")
            time.sleep(5)

def fill_form(no_x, no_y):
    print("Filling form...")

    paste(STUDENT_NUMBER)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(FULL_NAME)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(EMAIL)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(CELL)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(EMERGENCY)
    pyautogui.press('tab')
    time.sleep(0.2)

    # Click No for lifts
    print("Selecting No for lifts...")
    pyautogui.click(no_x, no_y)
    time.sleep(0.3)

    # Comments
    pyautogui.press('tab')
    time.sleep(0.2)
    paste(COMMENTS)
    time.sleep(0.2)

    print("All fields filled! Standing by to submit...")


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
        auto_login(driver, wait)

        # Wait until actually logged in
        wait_for_login(driver)
        time.sleep(1)

        # Navigate to signup page
        print("Navigating to Event Signups...")
        driver.get(PAGE_URL)
        time.sleep(2)

        notify("MSC Signup", "Page loaded! Select your event then press Enter in terminal.")

        print()
        print("="*50)
        print("PAGE IS READY!")
        print("="*50)
        print("1. Select the event you want")
        print("2. Press Enter here in the terminal")
        print()
        input("Press Enter once you have selected your event...")

        # Get No button coordinates
        no_x, no_y = NO_X, NO_Y

        # Countdown to click Student Number field
        print()
        print("You have 10 seconds to click the Student Number field!")
        for i in range(10, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("Filling now!")

        # Fill form
        fill_form(no_x, no_y)

        # Wait until exact signup time then submit
        wait_until_signup_time()

        print("Submitting!")
        time.sleep(0.4)
        pyautogui.press('enter')

        time.sleep(2)
        notify("MSC Signup", "Form submitted! Check browser to confirm.")

        print("="*50)
        print("DONE! Check browser to confirm.")
        print("="*50)
        print("Browser will close automatically in 30 seconds...")
        for i in range(30, 0, -5):
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