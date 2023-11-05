from configparser import ConfigParser
import os
from src import log
# Scraping functions
from src.data.scrape_users import gather_user_ids
from src.data.save_user_ids import save_raw_ids
from src.data.setup_webdriver import initialize_webdriver
from src.data.goodreads_login import login





def make_ids():

    # Path to directory for chrome driver and app
    chrome_tools_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'chrome_tools'
            )
        )
    
    # Path to directory for User IDs
    raw_data_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'data',
            'raw'
            )
        )
    
    # Find credentials
    config = ConfigParser()
    config.read('config.ini')
    username = config.get('credentials', 'username')
    password = config.get('credentials', 'password')

    try:

        # Configure driver
        driver = initialize_webdriver(chrome_tools_path)
        authenticated_driver = login(driver, username, password)

        # Scrape user IDs
        user_ids = gather_user_ids(authenticated_driver)
        
        save_raw_ids(user_ids, raw_data_path)

    except Exception as e:
        log.debug(f'An error occurred during the ID generation process: {e}')
        
    finally:
        if authenticated_driver:
            authenticated_driver.quit()

if __name__ == '__main__':
    make_ids()