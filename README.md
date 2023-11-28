Capstone 3: Book Recommendation System
==============================

Building a book recommendation system in Python

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks for exploring data and testing functions.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── make_X.py
    │   │   └── make_input.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

The purpose of this project was to create a dataset of books and ratings from Goodreads.com from which to recommend books to new users. The first challenge was the creation of the database. I created a webscraper to access many of Goodreads' most popular users' "Read" shelves and scrape 100 reviews. I consolidated these reviews into a database of over 50,000 records. I then trained an SVD model on the dataset using the scikit-surprise library. Unfortunately, this dataset was not sufficiently diverse and resulted in the model suggesting Harry Potter for every reader.

I brought in the Goodbooks dataset (https://github.com/zygmuntz/goodbooks-10k/tree/master) and integrated it into my recommendation algorithm. With almost 6 million records, I could afford to filter the dataset into a much smaller subset containing users who had common books with the new user, and then train the SVD model.
The project is deployed on Streamlit and links each recommendation to Goodreads.
Planned modifications include:
* Better error handling and exceptions
* Filtering for series so the model doesn't recommend books from a series the user is already familiar with (and doesn't recommend book #6, for example, instead of book #1)

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
