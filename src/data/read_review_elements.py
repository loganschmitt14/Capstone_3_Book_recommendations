from src import log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import numpy as np
def get_review(review_element):

    # Store cover URL if there is one
    try:
        cover_url = review_element.find_element(By.XPATH, './/img').get_attribute('src')
    except:
        cover_url = np.nan

    # Store title if there is one
    try:
        title_element = review_element.find_element(By.XPATH, ".//td[@class='field title']//a")
        title = title_element.text.strip()
    except Exception as e:
        title = np.nan    

    # Store author if there is one
    try:
        author_element = review_element.find_element(By.XPATH, ".//td[@class='field author']//a")
        author = author_element.text.strip()
    except:
        author = np.nan

    # Store ISBN if there is one
    try:
        isbn_element = review_element.find_element(By.XPATH, ".//td[@class='field isbn']//div[@class='value']")
        isbn = isbn_element.text.strip()
    except:
        isbn = np.nan

    # Store the ISBN13 if there is one
    try:
        isbn13_element = review_element.find_element(By.XPATH, ".//td[@class='field isbn13']//div[@class='value']")
        isbn13 = isbn13_element.text.strip()
    except:
        isbn13 = np.nan

    # Store the ASIN if there is one
    try:
        asin_element = review_element.find_element(By.XPATH, ".//td[@class='field asin']//div[@class='value']")
        asin = asin_element.text.strip()
    except:
        asin = np.nan
    
    # Store the average rating if there is one
    try:
        avg_rating_element = review_element.find_element(By.XPATH, ".//td[@class='field avg_rating']//div[@class='value']")
        avg_rating = np.float64(avg_rating_element.text.strip())
    except:
        avg_rating = 0

    # Store the user rating if there is one
    try:
        rating_container = review_element.find_element(By.XPATH, ".//td[@class='field rating']//div[@class='value']")
        # Find all the span elements with class indicating a full star (p10)
        full_stars = rating_container.find_elements(By.XPATH, ".//span[contains(@class, 'staticStar p10')]")
        # The rating is the number of full star spans
        rating = len(full_stars)
    except:
        rating = 0
    
    review = {'cover_url': cover_url, 'title': title, 'author': author, 'isbn': isbn, 'isbn13': isbn13, 'asin': asin, 'avg_rating': avg_rating, 'user_rating': rating,}
    return review