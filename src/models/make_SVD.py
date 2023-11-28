import os
import sqlite3
import pandas as pd
from surprise import Reader, Dataset, SVD
import numpy as np
from src.features.make_input import create_input_df
from src.models.make_user_df import make_df


def make_SVD_preds(database_path, book_ids):
    '''(Path, list) -> list
    Takes path to SQL database and list of book ids. Returns 5 book recommendations.
    '''
    conn = sqlite3.connect(database_path)
        
    input_df = create_input_df(conn, book_ids)
    print(len(input_df))

    best_SVD = SVD(n_factors = 10,
                   n_epochs = 20,
                   lr_all = 0.005,
                   reg_all = 0.02,
                   random_state = 14)

    user_df = make_df(book_ids)

    SVD_df = pd.concat([input_df, user_df], ignore_index = True)

    reader = Reader(rating_scale = (0, 5))

    data = Dataset.load_from_df(SVD_df[['user_id', 'book_id', 'user_rating']], reader)

    trainset = data.build_full_trainset()

    best_SVD.fit(trainset)

    testset = trainset.build_anti_testset()

    predictions = best_SVD.test(testset)

    user_id = 42815143

    user_predictions = [pred for pred in predictions if str(pred.uid) == str(user_id)]

    user_predictions.sort(key=lambda x: x.est, reverse=True)

    top_recommendations = [pred.iid for pred in user_predictions[:6]]

    conn.close()
    
    return top_recommendations