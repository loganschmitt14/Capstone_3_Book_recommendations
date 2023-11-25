import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import os


# ------------- SETTINGS ---------------
page_title = 'Book Recommendations'
page_icon = ':books:'

layout = 'centered'

def create_connection(db_file):
    ''' create a database connection to the SQLite database
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.write(e)

    return conn

    
database_path = database_path = os.path.abspath(
            os.path.join(
                'data',
                'processed',
                'books.db'
                )
            )

X_path = os.path.abspath(
        os.path.join(
            'data',
            'processed',
            'X.csv'
            )
        )

def gather_books(conn):
    ''' Return a DataFrame of the Books table
    '''
    cur = conn.cursor()
    query = 'SELECT * FROM Books'
    books_df = pd.read_sql_query(query, conn)
    return books_df


def find_book_ids(book_options, books_df):
    '''(List) -> list
    Returns list of book ids from book titles
    '''

    book_ids = []
    
    for book in book_options:
        book_id = int(books_df[books_df['title'] == book]['book_id'].iloc[0])
        book_ids.append(book_id)
        
    return book_ids
    
# -----------------------------------------

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)

st.title(f'{page_title} {page_icon}')

conn = create_connection(database_path)

books_df = gather_books(conn)

book_options = books_df['title'].sort_values(ascending = True).reset_index(drop = True)

label = 'What are your favorite books? Choose at least 5.'

placeholder = 'Pick some books!'

book_options = st.multiselect(label = label, options = book_options, placeholder = placeholder)

book_ids = find_book_ids(book_options, books_df)

st.write(book_ids)


















conn.close()