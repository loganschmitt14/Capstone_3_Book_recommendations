# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Other imports
from configparser import ConfigParser
import logging
import time

# Configure logging
logging.basicConfig(filename='selenium.log', level=logging.INFO)

# Configure driver
chrome_driver_path = '../chromedriver/chromedriver-win32/chromedriver.exe'
service = Service(chrome_driver_path)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = '../chrome_for_testing/chrome-win32/chrome.exe'

driver = webdriver.Chrome(service = service, options = chrome_options)

# Find credentials
config = ConfigParser()
config.read('../config.ini')
username = config.get('credentials', 'username')
password = config.get('credentials', 'password')

try:

    # Open Goodreads
    driver.get('https://www.goodreads.com')
    logging.info('Opened Goodreads successfully.')
    
    # Navigate to the main sign-in options page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.LINK_TEXT, 'Sign In'))).click()
    
    logging.info('Reached sign-in options page.')
    
    # Navigate to the sign-in with email page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.LINK_TEXT, 'Sign in with email'))).click()

    logging.info('Reached sign-in with email page.')

    
    # Input the username
    username_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.ID, 'ap_email')))

    username_field.send_keys(username)
    
    # Input the password
    password_field = driver.find_element(By.ID, 'ap_password')
    password_field.send_keys(password)
    
    # Submit the form to log in
    sign_in_button = driver.find_element(By.ID, 'signInSubmit')
    sign_in_button.click()

    logging.info("Login attempted.")

except NoSuchElementException as e:
    logging.error(f"Element not found: {e}")
    driver.save_screenshot('NoSuchElement.png')
except TimeoutException as e:
    logging.error(f"Timeout occurred: {e}")
    driver.save_screenshot('Timeout.png')
except Exception as e:
    logging.error(f"An error occurred: {e}")
    driver.save_screenshot(f'Exception_{int(time.time())}.png')

finally:
    driver.quit()
