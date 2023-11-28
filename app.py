import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import os
from src.models.make_user_df import make_df 
from src.models.make_predictions import predict_5

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
    ''' (SQLite Connection) -> DataFrame
    Return a DataFrame of the Books table
    '''
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


def make_recommendations(book_ids, X_path):
    '''(List) -> List
    Returns a list of book recommendations from a list of liked books.
    '''
    with st.spinner('Calculating...'):
        user_df = make_df(book_ids)

        recs_df = predict_5(user_df, X_path)

    return recs_df

def render_books(conn, output):
    ''' (SQLite connection, list) -> DataFrame
    Return a DataFrame of recommended books.
    '''
    books_df = pd.DataFrame()
    for book in output:
        book_df = pd.DataFrame()
        query = f'SELECT book_id, title, author, cover_url FROM BOOKS WHERE book_id = {book}'
        book_df = pd.read_sql_query(query, conn)
        books_df = pd.concat([books_df, book_df])
        
    return books_df
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

if 'predicted' not in st.session_state:
    output = tuple()
    st.session_state.predicted = {}

if st.button('Recommend!'):
    recs = make_recommendations(book_ids, X_path)
    input = str(tuple(book_ids))
    output = tuple(recs)
    st.session_state.predicted[input] = output
    st.write(st.session_state.predicted[input])
    books_df = render_books(conn, output)
    st.write(books_df)
        


















conn.close()