from src import log
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

def scroll_to_bottom(authenticated_driver):

    while True:
        authenticated_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')    
    
        try:
            status_element = WebDriverWait(authenticated_driver, 10).until(
                        EC.visibility_of_element_located((By.ID, 'infiniteStatus')))
            
            status_text = status_element.text

            loaded, total = map(int, re.findall(r'\d+', status_text))
    
            if loaded >= total:
                log.info('All items loaded.')
                break

        except TimeoutException:
            # If there's a timeout, assume we've hit the bottom
            log.debug('Timeout occurred while waiting for the infinite scroll content to load.')
            break

        except ValueError:
            # If for some reason we don't get two numbers, log an error and exit
            log.error('Could not extract loading status numbers.')
            break