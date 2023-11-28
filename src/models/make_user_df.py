import pandas as pd

def make_df(book_ids):
    '''(list) -> DataFrame
    Takes a list of Book IDs and returns a DataFrame with columns user_id,
    book_id, user_rating.
    '''
    
    user_id = 42815143
    rating = 5
    
    user_df = pd.DataFrame({'user_id': user_id, 'book_id': book_ids, 'user_rating': rating})
    
    return user_df