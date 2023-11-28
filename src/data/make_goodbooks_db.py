import sqlite3
import os
from pathlib import Path
import pandas as pd


def create_database(data_path, database_path):
    
    # Path to books.csv
    books_csv_path = os.path.abspath(os.path.join(data_path, 'books.csv'))
    
    # Path to ratings.csv
    ratings_csv_path = os.path.abspath(os.path.join(data_path, 'ratings.csv'))
    
    # Read books data into Pandas
    books_df = pd.read_csv(books_csv_path, usecols = ['book_id', 'best_book_id', 'authors', 'title', 'image_url'])
    
    # Read ratings data into Pandas
    ratings_df = pd.read_csv(ratings_csv_path)
    
    # Create SQLite connection
    with sqlite3.connect(database_path) as conn:

    # Create tables for Books and Ratings
        conn.execute('''CREATE TABLE IF NOT EXISTS Books
        (book_id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        goodreads_id TEXT,
        cover_url TEXT)''')
        
        
        conn.execute('''CREATE TABLE IF NOT EXISTS Ratings
        (user_id INTEGER,
        book_id INTEGER,
        user_rating INTEGER,
        FOREIGN KEY(book_id) REFERENCES Books(book_id))''')

        # Matching table schema
        books_df.rename(columns={
           'best_book_id': 'goodreads_id',
           'authors': 'author',
           'image_url': 'cover_url'
        }, inplace=True)
        
        # Bulk insert data into Books table
        books_df.to_sql('Books', conn, if_exists='replace', index=False)
        
        
        # Matching table schema
        ratings_df.rename(columns={'rating': 'user_rating'}, inplace=True)
        
        # BUlk insert data into Ratings table
        ratings_df.to_sql('Ratings', conn, if_exists='replace', index=False)
            




if __name__ == '__main__':

    data_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir,
                'data',
                'external'
                )
            )

    database_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir,
                'data',
                'processed',
                'goodbooks.db'
                )
            )

    create_database(data_path, database_path)