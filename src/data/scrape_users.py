# Administrative imports
from src import log
# Goodreads User ID scraping functions
from src.data.top_readers import get_top_reader_ids
from src.data.top_reviewers import get_top_reviewer_ids
from src.data.popular_reviewers import get_popular_reviewer_ids
from src.data.top_librarians import get_top_librarian_ids

def gather_user_ids(authenticated_driver):
    ''' (webdriver instance) -> tuple 
    Uses the authenticated driver to scrape each list of top users on Goodreads.
    '''
    try: 
        
        # Scrape, consolidate, and de-dupe user ID's
        user_id_set = set()
        user_id_set.update(get_top_librarian_ids(authenticated_driver))
        user_id_set.update(get_top_reader_ids(authenticated_driver))
        user_id_set.update(get_popular_reviewer_ids(authenticated_driver))
        user_id_set.update(get_top_reviewer_ids(authenticated_driver))

        # Convert set to tuple for immutability
        user_ids = tuple(user_id_set)

        log.info('Collected all user IDs.')

        return user_ids

    except Exception as e:
        log.debug(f'An error occurred while gathering user IDs: {e}')
        raise

    finally:
        if authenticated_driver is not None:
            authenticated_driver.quit()
