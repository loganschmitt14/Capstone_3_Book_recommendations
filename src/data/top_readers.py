# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Other imports
from src import log
from urllib.parse import urlparse, parse_qs

def get_top_reader_ids(driver):

    try:
        # Use a set because each profile link appears multiple times
        user_ids = set()
        
        driver.get('https://www.goodreads.com/user/top_readers?country=US&duration=a')
        log.info('Reached Top Readers page.')
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'mainContent')))

        # Get my user ID so I can remove it from the set later
        my_books_button = driver.find_element(By.LINK_TEXT, 'My Books')
        my_books_url = my_books_button.get_attribute('href')   
        # Parse the URL to get the user ID
        my_parsed_url = urlparse(my_books_url)
        # Remove path portion of URL
        my_user_id_text = my_parsed_url.path.split('/')[-1] 
        # Remove trailing words and characters
        my_user_id = my_user_id_text.split('-')[0] 
    
        # Find all the profile links by a consistent pattern or element
        profile_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/user/show/')]")
    
        # Loop through the links and extract the user IDs
        for link in profile_links:
            url = link.get_attribute('href')
            
            # Parse the URL to get the user ID
            parsed_url = urlparse(url)
    
            # Remove path portion of URL
            user_id_text = parsed_url.path.split('/')[-1]
    
            # Remove trailing words and characters
            user_id = user_id_text.split('-')[0]
    
            # Add the user ID to the set
            user_ids.add(user_id)

        log.info('Finished scraping Top Readers.')

        # Remove my user ID
        user_ids.remove(my_user_id)
        
        # Tuple for immutability
        return tuple(user_ids)

    # Log any exceptions and quit the driver
    except NoSuchElementException as e:
        log.debug(f'Element not found: {e}')
        driver.quit()
        
    except TimeoutException as e:
        log.debug(f'Timeout occurred: {e}')
        driver.quit()
        
    except Exception as e:
        log.debug(f'An error occurred: {e}')
        driver.quit()