import pandas as pd
import sqlite3
import numpy as np
import os
from pathlib import Path

def make_X_data(database_path, X_path):
    '''(Path, Path) -> CSV
    Accepts path to books.db database and desired output directory.
    Saves a CSV to output directory with feature engineered data.
    '''
    
    conn = sqlite3.connect(database_path)
    
    query = 'SELECT user_id, book_id, user_rating FROM Ratings'

    ratings_df = pd.read_sql_query(query, conn)

    conn.close()

    min_ratings = 99
    
    filter_users = ratings_df['user_id'].value_counts() >= min_ratings
    
    filter_users = filter_users[filter_users].index.to_list()
    
    filtered_ratings_df = ratings_df[ratings_df['user_id'].isin(filter_users)]

    filtered_ratings_df.to_csv(X_path, index = False)


if __name__ == '__main__':

    database_path = os.path.abspath(
            os.path.join(
                os.pardir,
                os.pardir,
                'data',
                'processed',
                'books.db'
                )
            )


    X_path = os.path.abspath(
        os.path.join(
            os.pardir,
            os.pardir,
            'data',
            'processed',
            'X.csv'
            )
        )


    make_X_data(database_path, X_path)









