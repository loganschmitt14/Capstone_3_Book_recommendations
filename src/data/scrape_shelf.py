from src import log
from src.data.adjust_shelf import adjust_shelf_settings
from src.data.scroll_down import scroll_to_bottom
from src.data.read_review_elements import get_review
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import polars as pl
import numpy as np
import time
from tqdm import tqdm

def scrape_user_read_shelf(authenticated_driver, user_id):

    base_url = 'https://www.goodreads.com/review/list/'
    url_ext = '?utf8=✓&shelf=read&sort=num_ratings&order=d&per_page=100'
    user_shelf_url = f'{base_url}{user_id}{url_ext}'

    try: 
        authenticated_driver.get(user_shelf_url)
        adjust_shelf_settings(authenticated_driver)
        #scroll_to_bottom(authenticated_driver)
        
        reviews_start = time.time()
        review_elements = authenticated_driver.find_elements(By.CLASS_NAME, 'bookalike.review')


        reviews = [get_review(review_element) for review_element in tqdm(review_elements)]
        
        reviews_df = pl.DataFrame(reviews).with_columns(pl.lit(user_id).alias('user_id'))

        reviews_stop = time.time()
        reviews_time = reviews_stop - reviews_start
        
        log.info(f"Compiled reviews. {time.strftime('%M:%S', time.gmtime(reviews_time))}")
    except Exception as e:
        log.debug(f'An error occurred while scraping user {user_id}: {e}')
        raise

    return reviews_df
