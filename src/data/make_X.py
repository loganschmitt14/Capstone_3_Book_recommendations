import pandas as pd
import sqlite3
import numpy as np
import os
from pathlib import Path


database_path = os.path.abspath(
            os.path.join(
                os.pardir,
                os.pardir,
                'data',
                'processed',
                'books.db'
                )
            )

def make_X_data(database_path, X_path):
    
    conn = sqlite3.connect(database_path)
    
    query = 'SELECT user_id, book_id, user_rating FROM Ratings'

    ratings_df = pd.read_sql_query(query, conn)

    conn.close()

    ratings_df['standardized_rating'] = ratings_df.groupby('user_id')['user_rating'].transform(standardize_ratings)