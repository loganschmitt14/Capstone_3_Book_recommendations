'''
Code based on the tutorial "Setting up Python logging for a library/app"
Author: João M.C. Teixeira
Date: 5/9/2020
Updated: 9/18/2021
URL: https://dev.to/joaomcteixeira/setting-up-python-logging-for-a-library-app-6ml
Used to format the log for the Capstone project.
'''

# Debug file formatter
DEBUGFORMATTER = '%(filename)s:%(name)s:%(funcName)s:%(lineno)d: %(message)s'

#Log file and stream output formatter
INFOFORMATTER = '%(message)s'

# Configuring log files for users
def init_log_files(log, mode='w'):
    '''
    Initiate log files.

    Two files are initiated:

    1. :py:attr:`myapp.logger.DEBUGFILE`
    2. :py:attr:`myapp.logger.INFOFILE`

    Adds the two files as log Handlers to :py:attr:`log`.

    Parameters
    ----------
    mode : str, (``'w'``, ``'a'``)
        The writing mode to the log files.
        Defaults to ``'w'``, overwrites previous files.    
    '''
    # Log for each handler
    db = logging.FileHandler(DEBUGFILE, mode=mode)
    db.setLevel(logging.DEBUG)
    db.setFormatter(logging.Formatter(DEBUGFORMATTER))

    info = logging.FileHandler(INFOFILE, mode=mode)
    info.setLevel(logging.INFO)
    info.setFormatter(logging.Formatter(INFOFORMATTER))

    log.addHandler(db)
    log.addHandler(info)