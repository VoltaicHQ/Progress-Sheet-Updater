import sys
import pickle
import os.path
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from errors import handle_error


def validate_sheet_range(str):
    valid_range = re.compile(r'(?P<sheet>.+)!(?P<col1>[A-Z]+)(?P<row1>\d+)(:(?P<col2>[A-Z]+)(?P<row2>\d+))?')
    return valid_range.match(str)


def read_sheet_range(api, id, sheet_range):
    try:
        response = (api.values()
                    .get(spreadsheetId=id, range=sheet_range)
                    .execute()
                    .get('values', [['0']]))

        # responses trim blank cells, act as if they are 0-filled
        m = validate_sheet_range(sheet_range)
        length = int(m.group('row2')) - int(m.group('row1')) + 1
        for lst in response:
            if len(lst) < 1:
                lst.append('0')
        flat = [val.strip().lower() for row in response for val in row]
        while len(flat) < length:
            flat.append('0')

        return flat

    except HttpError as error:
        handle_error('sheets_api', val=error._get_reason())


def write_to_cell(api, id, cell, val):
    try:
        api.values().update(spreadsheetId=id,
                            range=cell,
                            valueInputOption='RAW',
                            body={'values': [[val]]}).execute()
    except HttpError as error:
        handle_error('sheets_api', val=error._get_reason())


# https://developers.google.com/sheets/api/quickstart/python
def create_service():
    if not os.path.exists('credentials.json'):
        handle_error('no_credentials')

    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', cache_discovery=False, credentials=creds)
        return service.spreadsheets()
    except HttpError as error:
        handle_error('sheets_api', val=error._get_reason())
