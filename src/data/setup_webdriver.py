# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

def initialize_webdriver():
    try: 
        # Configure and initialize driver
        chrome_driver_path = '../chromedriver/chromedriver-win32/chromedriver.exe'
        service = Service(chrome_driver_path)
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = '../chrome_for_testing/chrome-win32/chrome.exe'
        
        driver = webdriver.Chrome(service = service, options = chrome_options)
        
        return driver
    
    except WebDriverException as e:
        print("An error occurred while setting up the WebDriver:", e)
        # Depending on the severity, you may want to exit the script or raise the exception
        raise

# If run as a standalone script
if __name__ == '__main__':
    try:
        driver = initialize_webdriver()
        # Navigate to a test site for 20 seconds
        driver.get('https://www.goodreads.com')
        time.sleep(20)
    except Exception as e:
        print("An error occurred during the WebDriver test:", e)
    finally:
        
        if driver is not None:
            driver.quit()




