import sqlite3
import pandas as pd

def create_input_df(conn, book_ids):
    ''' (Database connection, list) -> DataFrame
    Takes a list of book ids and a database connection and returns 
    a dataframe with all ratings from users who have rated at least 3 items
    from the list.
    
    '''
    # Convert the list of book_ids to a string format for SQL query
    formatted_book_ids = ','.join([str(id) for id in book_ids])

    # SQL query to find users who have rated at least two books in the list
    users_who_read_at_least_two_books_query = f'''
    SELECT user_id
    FROM ratings
    WHERE book_id IN ({formatted_book_ids})
    GROUP BY user_id
    HAVING COUNT(DISTINCT book_id) >= 3
    '''

    # SQL query to retrieve all ratings from users who have rated at least two books in the list
    user_ratings_query = f'''
    SELECT r.*
    FROM ratings r
    WHERE r.user_id IN ({users_who_read_at_least_two_books_query})
    LIMIT 50000
    '''

    # Execute the query and return the results in a DataFrame
    input_df = pd.read_sql(user_ratings_query, conn)

    # Close the connection
    conn.close()

    return input_df
