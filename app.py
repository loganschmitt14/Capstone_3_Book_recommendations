import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import os
import requests
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_lottie import st_lottie
import contextlib
from src.models.make_user_df import make_df 
from src.models.make_predictions import predict_5
from src.models.make_SVD import make_SVD_preds

# ------------- SETTINGS ---------------
page_title = 'Book Recommendations'
page_icon = ':books:'

layout = 'centered'

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()





@contextlib.contextmanager
def create_connection(database_path):
    ''' (Database Path) -> SQLite connection 
    Create a database connection to the SQLite database
    '''
    conn = None
    try:
        conn = sqlite3.connect(database_path)
        #st.write('Successful connection')
        yield conn
    except Exception as e:
        st.write(e)
        raise
    finally:
        if conn:
            conn.close()
            #st.write('Database connection closed')



goodbooks_path = os.path.abspath(
            os.path.join(
                'data',
                'processed',
                'goodbooks.db'
                )
            )

mybooks_path = os.path.abspath(
            os.path.join(
                'data',
                'processed',
                'books.db'
                )
            )


@st.cache_data
def gather_books(database_path):
    ''' (Database Path) -> DataFrame
    Return a DataFrame of the Books table
    '''
    with create_connection(database_path) as conn:
    
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


def make_recommendations(database_path, book_ids):
    '''(Databse Path, List) -> List
    Returns a list of book recommendations from a list of liked books.
    '''
    with st.spinner('Calculating...'):
        recs_df = make_SVD_preds(database_path, book_ids)

    return recs_df

def collect_books(database_path, output):
    ''' (Database Path, list) -> DataFrame
    Return a DataFrame of recommended books.
    '''
    preds_df = pd.DataFrame()
    with create_connection(database_path) as conn:
        for book in output:
            pred_df = pd.DataFrame()
            query = f'SELECT book_id, title, author, cover_url, goodreads_id FROM BOOKS WHERE book_id = {book}'
            pred_df = pd.read_sql_query(query, conn)
            preds_df = pd.concat([preds_df, pred_df])
        
    return preds_df
# -----------------------------------------

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)

lottie_book = load_lottieurl("https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json")
st_lottie(lottie_book, speed = 1, height = 200, key="initial")

st.title('Goodreads Book Recommendations')

st.session_state['predicted'] = False

# conn = create_connection(goodbooks_path)

books_df = gather_books(goodbooks_path)

book_options = books_df['title'].sort_values(ascending = True).reset_index(drop = True)

row_1 = st.columns([7, 3], gap = 'medium')

with row_1[0]:

    label = 'What are your favorite books? Choose at least 5.'

    placeholder = 'Start typing...'

    book_options = st.multiselect(label = label, options = book_options, placeholder = placeholder)

book_ids = find_book_ids(book_options, books_df)


if st.session_state.predicted == False:
    output = tuple()

with row_1[1]:
    add_vertical_space(3)
    if len(book_ids) >= 5:
        if st.button('Recommend!'):
            recs = make_recommendations(goodbooks_path, book_ids)
            input = str(tuple(book_ids))
            output = tuple(recs)
            st.session_state.predicted = True
            #st.write(st.session_state.predicted[input])
            preds_df = collect_books(goodbooks_path, output)
            #st.write(preds_df)


st.write('\n \n')


if st.session_state.predicted == True:
    st.header('Recommendations:')
    preds_df = preds_df.reset_index(drop=True)

    if len(preds_df) >= 6:
        row1 = st.columns(3)
        row2 = st.columns(3)
        
        for index, book in preds_df.iterrows():
            col = row1[index] if index < 3 else row2[index - 3]
            with col:
                book_url = f"https://www.goodreads.com/book/show/{book['goodreads_id']}"
                # Displaying the book cover image
                st.image(book['cover_url'], width=150)

                # Creating a Markdown string for the title and author as clickable links
                markdown_link = f"[{book['title']} by {book['author']}]({book_url})"
                st.markdown(markdown_link, unsafe_allow_html=True)


 




