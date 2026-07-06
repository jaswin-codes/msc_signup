from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pyperclip
import time
from datetime import datetime


def notify(title, message):
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

def auto_login(driver, wait, uct_username, uct_password):
    try:
        print("Clicking UCT LOGIN button...")
        uct_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.d2l-button")
        ))
        uct_btn.click()
        time.sleep(2)

        print("Entering username...")
        username_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='email'], input[name='loginfmt']")
        ))
        username_field.clear()
        username_field.send_keys(uct_username)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)

        print("Entering password...")
        password_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='password']")
        ))
        password_field.clear()
        password_field.send_keys(uct_password)
        time.sleep(0.5)
        pyautogui.press('enter')
        print("Credentials entered! Approve Authenticator on your phone...")
        notify("MSC Signup", "Approve Microsoft Authenticator now!")

    except Exception as e:
        print(f"Auto-login failed ({e}), please log in manually...")
        notify("MSC Signup", "Auto-login failed - please log in manually!")

def wait_until_signup_time(signup_time):
    target = datetime.strptime(signup_time, "%Y-%m-%d %H:%M:%S")
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

def fill_form(student_number, full_name, email, cell, emergency, comments, no_x, no_y):
    print("Filling form...")

    paste(student_number)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(full_name)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(email)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(cell)
    pyautogui.press('tab')
    time.sleep(0.2)

    paste(emergency)
    pyautogui.press('tab')
    time.sleep(0.2)

    print("Selecting No for lifts...")
    pyautogui.click(no_x, no_y)
    time.sleep(0.3)

    pyautogui.press('tab')
    time.sleep(0.2)
    paste(comments)
    time.sleep(0.2)

    print("All fields filled! Standing by to submit...")