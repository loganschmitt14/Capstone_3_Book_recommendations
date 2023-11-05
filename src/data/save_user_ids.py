from src import log
import os
import pickle

def save_raw_ids(user_ids, raw_data_path):

    try:
              
        # Ensure the directory exists
        os.makedirs(raw_data_path, exist_ok=True)  
        log.info('The raw data directory exists')
        
        # Save the data to the specified directory
        user_ids_file_path = os.path.join(raw_data_path, 'user_ids.pkl')
        with open(user_ids_file_path, 'wb') as f:
            pickle.dump(user_ids, f)

        log.info(f'Saved user IDs to {user_ids_file_path}')


    except Exception as e:
        log.debug(f'An error ocurred while saving the user IDs.')
        raise
