# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Other imports
from src import log

def login(driver, username, password):
    ''' Use the initialized driver to sign into goodreads.com 
    with the provided credentials. Return the driver. 
    '''
    try:
        # Open Goodreads
        driver.get('https://www.goodreads.com')
        log.info('Opened Goodreads successfully.')
        
        # Navigate to the main sign-in options page
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.LINK_TEXT, 'Sign In'))).click()
        
        log.info('Reached sign-in options page.')
        
        # Navigate to the sign-in with email page
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.LINK_TEXT, 'Sign in with email'))).click()
    
        log.info('Reached sign-in with email page.')
    
        # Input the username
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.ID, 'ap_email')))
    
        username_field.send_keys(username)
        
        # Input the password
        password_field = driver.find_element(By.ID, 'ap_password')
        password_field.send_keys(password)
        
        # Submit the form to log in
        sign_in_button = driver.find_element(By.ID, 'signInSubmit')
        sign_in_button.click()
    
        log.info('Login attempted.')

        # Confirm login was successful
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'personalNav')))
        
        log.info('Login successful.')

        return driver

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

