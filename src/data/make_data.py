import polars as pl
import pickle
import os
import time
from configparser import ConfigParser
from pathlib import Path
from tqdm import tqdm
# Webscraping functions
from src.data.scrape_shelf import scrape_user_read_shelf
from src.data.setup_webdriver import initialize_webdriver
from src.data.goodreads_login import login
from src import log


# Function to save the DataFrame to a file
def save_dataframe(df, filepath):
    try:
        df.write_csv(filepath)
    except Exception as e:
        log.debug(f'Could not save to {filepath}.')
        raise

# Function to import the user IDs
def load_user_ids(filepath):
    with open(filepath, 'rb') as file:
        user_ids = pickle.load(file)
    return user_ids

def make_data():

    # Path to data/raw folder
    raw_data_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir,
                'data',
                'raw'
                )
            )

    # Path to directory for chrome driver and app
    chrome_tools_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'chrome_tools'
            )
        )
    
    
    # Load in User ID file
    user_ids_path = os.path.join(raw_data_path, 'user_ids.pkl')
    user_ids = load_user_ids(user_ids_path)

    halfway_point = len(user_ids) // 2
    laptop_users = user_ids[:halfway_point]
    desktop_users = user_ids[halfway_point:]
    
    # Load configuration for login
    config = ConfigParser()
    config.read('config.ini')
    username = config.get('credentials', 'username')
    password = config.get('credentials', 'password')

    # Track which users have been scraped
    scraped_users_file = scraped_users_file = Path(raw_data_path) / 'scraped_users.txt'
    if scraped_users_file.exists():
        scraped_users = set(scraped_users_file.read_text().splitlines())
    else:
        scraped_users = set()

    # Initialize WebDriver and login
    driver = initialize_webdriver(chrome_tools_path)
    authenticated_driver = login(driver, username, password)

    # Scrape in batches
    for user_id in desktop_users:
        if user_id not in scraped_users:
            try:
                # Scrape the user's read shelf
                user_df = scrape_user_read_shelf(authenticated_driver, user_id)

                user_file = os.path.join(raw_data_path, f'{user_id}.csv')
                
                save_dataframe(user_df, user_file)

                log.info(f'Data for user {user_id} saved.')

                # Update the scraped users list
                with scraped_users_file.open('a') as file:
                    file.write(user_id + '\n')

                # Implement a delay to avoid rate limiting
                time.sleep(2)

            except Exception as e:
                # Log the error and potentially retry or skip this user
                log.exception(f'An error occurred while scraping user {user_id}: {e}')

    # Close the driver once all users have been processed
    driver.quit()
    log.info('Completed scraping all user read shelves.')

if __name__ == '__main__':
    make_data()
