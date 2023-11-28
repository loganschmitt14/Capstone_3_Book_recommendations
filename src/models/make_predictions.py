import pandas as pd
import os
from pathlib import Path
import numpy as np
import random
import surprise
from surprise import Reader, Dataset
from surprise import SVDpp, SVD
from collections import defaultdict



X_path = os.path.abspath(
        os.path.join(
            os.pardir,
            os.pardir,
            'data',
            'processed',
            'X.csv'
            )
        )

def predict_5(user_df, X_path):
    '''(DataFrame) -> list
    Takes the user's favorite books as an input and recommends 5 books as an output
    '''

    best_SVD = SVD(n_factors = 10, n_epochs = 20,  lr_all = 0.005, reg_all = 0.02, random_state = 14)

    X = pd.read_csv(X_path)
    
    X_add = pd.concat([X, user_df], ignore_index = True)
    
    reader = Reader(rating_scale = (0, 5))
    
    data = Dataset.load_from_df(X_add[['user_id', 'book_id', 'user_rating']], reader)
    
    trainset = data.build_full_trainset()

    best_SVD.fit(trainset)
    
    testset = trainset.build_anti_testset()
    
    predictions = best_SVD.test(testset)
    
    user_id = 42815143
    
    user_predictions = [pred for pred in predictions if str(pred.uid) == str(user_id)]
    
    user_predictions.sort(key=lambda x: x.est, reverse=True)
    
    top_recommendations = [pred.iid for pred in random.sample(user_predictions[:50], 5)]
    
    return top_recommendations