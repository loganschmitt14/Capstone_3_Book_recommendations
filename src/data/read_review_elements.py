from src import log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import numpy as np
def get_review(review_element):

    # Store the title
    try:
        title_element = review_element.find_element(By.XPATH, ".//td[@class='field title']//a")
        title = title_element.text.strip()
        
    except Exception as e:
        log.debug(f'An error occurred while extracting book title: {e}')
        title = np.nan
        
    # Store the average rating if there is one
    try:
        avg_rating_element = review_element.find_element(By.XPATH, 
                                                         ".//td[@class='field avg_rating']//div[@class='value']")
        avg_rating = np.float64(avg_rating_element.text.strip())
        
    except:
        avg_rating = np.float64(0)

        
     # Store author if there is one
    try:
        author_element = review_element.find_element(By.XPATH, ".//td[@class='field author']//a")
        author = author_element.text.strip()
    except:
        author = np.nan
    # Store the user rating if there is one
    try:
        rating_container = review_element.find_element(By.XPATH,
                                                       ".//td[@class='field rating']//div[@class='value']")
        
        # Find all the span elements with class indicating a full star (p10)
        full_stars = rating_container.find_elements(By.XPATH, 
                                                    ".//span[contains(@class, 'staticStar p10')]")
        
        # The rating is the number of full star spans
        user_rating = len(full_stars)
    except:
        rating = 0
        
    # Store the URL for the cover image
    try:
        cover_url = review_element.find_element(By.XPATH, './/img').get_attribute('src')
    except:
        cover_url = np.nan

    review = {'title': title, 'author': author, 'avg_rating': avg_rating, 'user_rating': user_rating, 'cover_url': cover_url}
    
    return review