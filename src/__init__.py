'''
Code based on the tutorial "Setting up Python logging for a library/app"
Author: João M.C. Teixeira
Date: 5/9/2020
Updated: 9/18/2021
URL: https://dev.to/joaomcteixeira/setting-up-python-logging-for-a-library-app-6ml
Used to establish a log for the Capstone project.
'''

import logging

from src.logger import INFOFORMATTER

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# defines the stream handler
_ch = logging.StreamHandler()  # creates the handler
_ch.setLevel(logging.INFO)  # sets the handler info
_ch.setFormatter(logging.Formatter(INFOFORMATTER))  # sets the handler formatting

# adds the handler to the global variable: log
log.addHandler(_ch)


