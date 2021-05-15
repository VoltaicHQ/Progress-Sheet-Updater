import os
import pathlib
import sys

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    PROJECT_DIR = pathlib.Path(sys.executable).parent.absolute()
elif __file__:
    PROJECT_DIR = pathlib.Path(__file__).parent.absolute()
LOG_FILE_PATH = os.path.join(PROJECT_DIR, 'logging.conf')
SPREADSHEET_TOKEN_FILE_PATH = os.path.join(PROJECT_DIR, 'token.pickle')
SPREADSHEET_CREDENTIALS_FILE_PATH = os.path.join(PROJECT_DIR, 'credentials.json')
