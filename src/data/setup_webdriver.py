# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from src import log
import time

def initialize_webdriver(chrome_tools_path):
    try: 
        # Configure and initialize driver
        chrome_driver_path = (chrome_tools_path + '/chromedriver/chromedriver-win32/chromedriver.exe')
        service = Service(chrome_driver_path)
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = (chrome_tools_path + '/chrome_for_testing/chrome-win32/chrome.exe')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--allow-running-insecure-content")
        
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #chrome_options.add_argument('--headless=new')
        
        driver = webdriver.Chrome(service = service, options = chrome_options)
        log.info('Successfully launched webdriver')
        
        return driver
    
    except WebDriverException as e:
        print("An error occurred while setting up the WebDriver:", e)
        log.debug
        # Depending on the severity, you may want to exit the script or raise the exception
        raise

# If run as a standalone script
if __name__ == '__main__':
    try:
        driver = initialize_webdriver(chrome_tools_path = '../../chrome_tools')
        # Navigate to a test site for 20 seconds
        driver.get('https://www.goodreads.com')
        time.sleep(20)
    except Exception as e:
        print("An error occurred during the WebDriver test:", e)
    finally:
        if driver is not None:
            driver.quit()




