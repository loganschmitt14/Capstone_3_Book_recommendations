from src import log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

def adjust_shelf_settings(authenticated_driver):
    try:
        settings_button = WebDriverWait(authenticated_driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'shelfSettingsLink')))
        settings_button.click()
        log.info('Opened shelf settings.')

        select_checkbox_ids = ('asin', 'author', 'avg_rating', 'cover',
                        'isbn', 'isbn13', 'rating', 'title'
                       )

        deselect_checkbox_ids = ('date_read', 'date_added', 'shelves')

        for checkbox in select_checkbox_ids:
            checkbox_name = f'shelf[display_fields][{checkbox}]'
            checkbox_to_select = WebDriverWait(authenticated_driver, 10).until(
                EC.element_to_be_clickable((By.NAME, checkbox_name)))
            if not checkbox_to_select.is_selected():
                checkbox_to_select.click()

        for checkbox in deselect_checkbox_ids:
            checkbox_name = f'shelf[display_fields][{checkbox}]'
            checkbox_to_select = WebDriverWait(authenticated_driver, 10).until(
                EC.element_to_be_clickable((By.NAME, checkbox_name)))
            if checkbox_to_select.is_selected():
                checkbox_to_select.click()

        settings_button.click()
        
        log.info('Settings adjusted. Closed settings panel.')
        
    except Exception as e:
        log.debug(f'An error occurred while adjusting shelf settings: {e}')
        raise