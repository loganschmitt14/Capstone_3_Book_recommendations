from src import log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import numpy as np
def get_review(review_element):

    try:
        book_elements = review_element.find_elements(By.XPATH, ".//a[contains(@href, '/book/show/')]")
        book_url = book_elements[0].get_attribute('href')
        
    except Exception as e:
        log.debug(f'An error occurred while extracting book URL: {e}')
        book_url = np.nan



    # Store the average rating if there is one
    try:
        avg_rating_element = review_element.find_element(By.XPATH, 
                                                         ".//td[@class='fieldavg_rating']//div[@class='value']")
        avg_rating = np.float64(avg_rating_element.text.strip())
    except:
        avg_rating = 0

    # Store the user rating if there is one
    try:
        rating_container = review_element.find_element(By.XPATH,
                                                       ".//td[@class='field rating']//div[@class='value']")
        
        # Find all the span elements with class indicating a full star (p10)
        full_stars = rating_container.find_elements(By.XPATH, 
                                                    ".//span[contains(@class, 'staticStar p10')]")
        
        # The rating is the number of full star spans
        rating = len(full_stars)
    except:
        rating = 0
    
    review = {'book_url': book_url, 'avg_rating': avg_rating, 'user_rating': rating}
    
    return review