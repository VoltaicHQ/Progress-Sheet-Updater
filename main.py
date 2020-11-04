from getPath import *
import csv
import urllib.request
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import time
from colorama import Fore

# Read the Spreadsheet ID from the spreadsheetid.txt file
assert os.path.exists("spreadsheetid.txt"), "Could not find spreadsheetid.txt"
f = open("spreadsheetid.txt", "r")
BENCH_SPREADSHEET_ID = f.read()
f.close()
BENCH_RANGE_NAME = 'Benchmarks!F3:F22'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

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
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Check if path to stats folder was already given, if not create it
pr = Pathreader
path = pr.getpath(pr)

# Create a List of all files in the stats folder
allfiles = os.listdir(path)

# Read Benchmarks into a List (Thanks to Knar for helping me with this)
url = 'https://docs.google.com/spreadsheets/d/1xZXBuziZZKTbLR5uwP0-vlok0b07jv0mxXKgvHYPyB8/gviz/tq?tqx=out:csv&sheet' \
      '=Benchmarks '
response = urllib.request.urlopen(url)
lines = [l.decode('utf-8') for l in response.readlines()]
temp = csv.reader(lines)

# Create a List with all Benchmark Names and a list with the scores for all benchmarks
benchmarknames = []
benchmarkvalues = []
for row in temp:
    if row[1] != "Scenario":
        scenname = row[1]
        benchmarknames.append(scenname)
        scores = "{};{};{};{};{};{};{};{}\n"
        benchmarkvalues.append(scores.format(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

# Initialize list highscores
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=BENCH_SPREADSHEET_ID, range=BENCH_RANGE_NAME).execute()
highscores = result.get("values", [])


# Function to clear console window
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Run a while that stops on Ctrl+C press
try:
    while True:
        found = False
        allfilesupdated = os.listdir(path)
        s = set(allfiles)
        newentries = [x for x in allfilesupdated if x not in s]
        for entry in newentries:
            for bench in benchmarknames:
                entryname = entry[0:entry.find(" - Challenge - ")-1]
                if bench.lower() == entryname.lower():
                    changedbench = bench
                    f = open(path + "\\" + entry, "r")
                    content = f.read()
                    f.close()
                    seperatedlines = content.splitlines()
                    for line in seperatedlines:
                        if line.find("Score") != -1:
                            current = float(line[7:])
                            current = round(current, 1)
                            if current > highscores[benchmarknames.index(bench)]:
                                highscores[benchmarknames.index(bench)] = current
                                found = True
        cls()
        if found:
            values = [
                [
                    [highscores[0]],
                    [highscores[1]],
                    [highscores[2]],
                    [highscores[3]],
                    [highscores[4]],
                    [highscores[5]],
                    [highscores[6]],
                    [highscores[7]],
                    [highscores[8]],
                    [highscores[9]],
                    [highscores[10]],
                    [highscores[11]],
                    [highscores[12]],
                    [highscores[13]],
                    [highscores[14]],
                    [highscores[15]],
                    [highscores[16]],
                    [highscores[17]],
                    [highscores[18]],
                    [highscores[19]],

                ],
                # Additional rows ...
            ]
            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=BENCH_SPREADSHEET_ID, range=BENCH_RANGE_NAME,
                valueInputOption="RAW", body=body).execute()
            print("Progress Sheet Updater made by", end=" ")
            print(Fore.LIGHTGREEN_EX + "Yondaime")
            print(Fore.RESET + "Last update was at:", end=" ")
            print(Fore.BLUE + "{}".format(datetime.now().strftime("%H:%M:%S")))
            print(Fore.RESET + "The score of", end=" ")
            print(Fore.BLUE + bench, end=" ")
            print(Fore.RESET + "was updated")
            print(Fore.RESET + "Highscore is now", end=" ")
            print(Fore.BLUE + current)
            print(Fore.RESET + "To stop the program press", end=" ")
            print(Fore.RED + "[Ctrl+C]")
            print(Fore.RESET + "If you have questions try reading the Readme")

        else:
            print("Progress Sheet Updater made by", end=" ")
            print(Fore.LIGHTGREEN_EX + "Yondaime")
            print(Fore.RESET + "Last update was at:", end=" ")
            print(Fore.BLUE + "{}".format(datetime.now().strftime("%H:%M:%S")))
            print(Fore.RESET + "The score of", end=" ")
            print(Fore.BLUE + "no benchmark", end=" ")
            print(Fore.RESET + "was updated")
            print(Fore.RESET + "Highscore is", end=" ")
            print(Fore.BLUE + "the same")
            print(Fore.RESET + "To stop the program press", end=" ")
            print(Fore.RED + "[Ctrl+C]")
            print(Fore.RESET + "If you have questions try reading the Readme")
        time.sleep(60)
except KeyboardInterrupt:
    print("Exiting...")
    pass
