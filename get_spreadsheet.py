import os.path
from datetime import datetime
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import csv
import urllib.request
import sys


# This class handles creating the GoogleAPI Service and fetching the benchmark list
class spreadSheetReader:

    def read_spreadsheet_id(self):
        # Read the Spreadsheet ID from the spreadsheetid.txt file
        try:
            assert os.path.exists('spreadsheetlink.txt'), "Could not find spreadsheetlink.txt\n Error raised at " + \
                                                        datetime.now().strftime("%H:%M:%S")
            f = open("spreadsheetlink.txt", "r")
            idinput = f.read()
            f.close()
            bench_spreadsheet_id = idinput[idinput.find("/d/") + 3:idinput.find("/edit")]  # Extract the id from the
            return bench_spreadsheet_id                                                    # full link
        except AssertionError:
            f = open("error.txt", "w")
            f.write(
                "Could not find the spreadsheetlink.txt, make sure you place it into the same directory as your .exe")
            f.close()
            sys.exit()

    def check_spreadsheet_id(self, sheet_id):
        try:
            assert sheet_id != ""
        except AssertionError:
            f = open("error.txt", "w")
            f.write(
                "Your spreadsheetlink.txt file seems to be empty, make sure you save the file after pasting the "
                "spreadsheet link. ALso check if your link has the correct format")
            f.close()
            sys.exit()

    def create_service(self):
        try:
            assert os.path.exists("credentials.json")
        except AssertionError:
            f = open("error.txt", "w")
            f.write(
                "Your credentials.json file seems to not be in the right directory, make sure you move it into "
                "the folder that has the rest of the files.")
            f.close()
            sys.exit()
        # Set scopes for the GoogleAPI, if modifying these scopes, delete the file token.pickle.
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('sheets', 'v4', credentials=creds)
        return service

    def get_benchmarks(self):
        # Read Benchmarks into a List (Thanks to Knar for helping me with this)
        url = 'https://docs.google.com/spreadsheets/d/1xZXBuziZZKTbLR5uwP0-vlok0b07jv0mxXKgvHYPyB8/gviz/tq?tqx=out' \
              ':csv&sheet=Benchmarks '
        response = urllib.request.urlopen(url)
        lines = [li.decode('utf-8') for li in response.readlines()]
        sheet_rows = csv.reader(lines)
        # Create a List with all Benchmark Names
        benchmarknames = []
        for row in sheet_rows:
            if row[1] != "Scenario":
                scenname = row[1]
                benchmarknames.append(scenname)
        return benchmarknames
