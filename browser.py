from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import os
import shutil
import re
import argparse

def create_driver(headless_flag):
    chrome_options = Options()
    
    # Headless Mode
    if headless_flag:
        chrome_options.add_argument("--headless")  

    # Essential Chrome Options
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Disable Password Manager
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Inject JavaScript to Block Password Popups
    driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        window.addEventListener('load', () => {
            const warnings = document.querySelectorAll('div[role="dialog"]');
            warnings.forEach(warning => warning.remove());
        });
    """)

    return driver

# to make typing look human like for easier visual understanding
def visual_typing(element, text, headless_flag, delay=0.1):
    if headless_flag:
        element.send_keys(text)
    else:
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

def login(driver, driver_wait, TIMEOUT, headless_flag):
    driver.get(os.getenv("LOGIN_URL"))
    login_input_box = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div[2]/div[1]/div/div/form/div[1]/input""")))
    visual_typing(login_input_box, os.getenv("SAUCE_USERNAME"), headless_flag)
    time.sleep(TIMEOUT)
    login_password_box = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div[2]/div[1]/div/div/form/div[2]/input""")))
    visual_typing(login_password_box, os.getenv("SAUCE_PASSWORD"), headless_flag)
    time.sleep(TIMEOUT)
    login_button = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div[2]/div[1]/div/div/form/input""")))
    login_button.click()
    time.sleep(TIMEOUT)
    print("Logged in")

def place_order(driver, driver_wait, TIMEOUT, headless_flag):
    item_filter = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[1]/div[2]/div/span/select""")))
    item_filter.click()
    time.sleep(TIMEOUT)
    price_low_high_filter = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[1]/div[2]/div/span/select/option[3]""")))
    price_low_high_filter.click()
    print("Filtered Items High to Low")
    time.sleep(TIMEOUT)
    first_item_add_to_cart = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/button""")))
    first_item_add_to_cart.click()
    print("First Item Added")
    time.sleep(TIMEOUT)
    second_item_add_to_cart = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/button""")))
    second_item_add_to_cart.click()
    print("Second Item Added")
    time.sleep(TIMEOUT)
    third_item_add_to_cart = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/div/div/div[3]/div[2]/div[2]/button""")))
    third_item_add_to_cart.click()
    print("Third Item Added")
    time.sleep(TIMEOUT)
    view_cart = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[1]/div[1]/div[3]/a""")))
    view_cart.click()
    time.sleep(TIMEOUT)
    checkout = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/div[2]/button[2]""")))
    checkout.click()
    time.sleep(TIMEOUT)
    first_name_input = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/form/div[1]/div[1]/input""")))
    visual_typing(first_name_input, os.getenv("FIRST_NAME"), headless_flag)
    time.sleep(TIMEOUT)
    last_name_input = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/form/div[1]/div[2]/input""")))
    visual_typing(last_name_input, os.getenv("LAST_NAME"), headless_flag)
    time.sleep(TIMEOUT)
    zip_code_input = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/form/div[1]/div[3]/input""")))
    visual_typing(zip_code_input, os.getenv("ZIP_CODE"), headless_flag)
    print("Billing Info entered")
    time.sleep(TIMEOUT)
    continue_button = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/form/div[2]/input""")))
    continue_button.click()
    time.sleep(TIMEOUT)
    finish_button = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/div/div[2]/div[9]/button[2]""")))
    # Scroll slowly to the bottom of the page if not in headless mode
    if not headless_flag:
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(0, scroll_height, 50):  # Scroll in increments of 50 pixels
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.05)  # Adjust for slower or faster scrolling
        print("Scrolled to the bottom of the page")
    finish_button.click()
    time.sleep(TIMEOUT)
    back_home_button = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[2]/button""")))
    back_home_button.click()
    print("Items ordered")
    time.sleep(TIMEOUT)

def signout(driver, driver_wait, TIMEOUT):
    sidebar = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[1]/div[1]/div[1]/div/div[1]/div/button""")))
    sidebar.click()
    time.sleep(TIMEOUT)
    logout = driver_wait.until(EC.visibility_of_element_located(("xpath", """/html/body/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/nav/a[3]""")))
    logout.click()
    print("loged out")
    time.sleep(TIMEOUT)

def main():
    # Argument parser to handle the headless flag
    parser = argparse.ArgumentParser(description="Browser automation script.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the browser in headless mode."
    )
    args = parser.parse_args()
    
    # Set the headless flag based on the terminal argument --headless
    headless_flag = args.headless
    TIMEOUT = 0
    if not headless_flag:
        TIMEOUT = 0.75

    # Start the timer
    start_time = time.time()

    try:
        # load in .env
        load_dotenv()
        browser_error_folder = os.path.join(os.getcwd(), "browser_errors")
        # Ensure the browser_errors directory exists
        os.makedirs(browser_error_folder, exist_ok=True)
        WAIT_IN_SECONDS = 60 * 10
        driver = create_driver(headless_flag)
        driver_wait = WebDriverWait(driver, WAIT_IN_SECONDS)
        login(driver, driver_wait, TIMEOUT, headless_flag)
        place_order(driver, driver_wait, TIMEOUT, headless_flag)
        signout(driver, driver_wait, TIMEOUT)
    except Exception as e:
        # Capture timestamped screenshot and save to local "browser_errors" folder
        timestamp = int(time.time())
        screenshot_filename = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(browser_error_folder, screenshot_filename)
        
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved locally to {screenshot_path}")

        # Re-raise the exception to allow higher-level handling if desired
        raise e
    finally:
        # Ensure the driver is closed even if an error occurs
        if driver:
            driver.quit()
        # End the timer and print the elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Script execution time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()