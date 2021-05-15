import os
import pathlib


PROJECT_DIR = pathlib.Path(__file__).parent.absolute()
LOG_FILE_PATH = os.path.join(PROJECT_DIR, 'logging.conf')
SPREADSHEET_TOKEN_FILE_PATH = os.path.join(PROJECT_DIR, 'token.pickle')
SPREADSHEET_CREDENTIALS_FILE_PATH = os.path.join(PROJECT_DIR, 'credentials.json')
