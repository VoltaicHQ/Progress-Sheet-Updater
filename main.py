from get_spreadsheet import spreadSheetReader
from get_output import consoleOutput
import sys
import os
import time
import json
import re
import csv
from googleapiclient.errors import HttpError

CONFIG = json.load(open("config.json", "r"))
SHEET_API = spreadSheetReader.create_service().spreadsheets()
SHEET_ID = spreadSheetReader.read_spreadsheet_id(CONFIG['link_to_sheet'])


def check_stats_path(path):
    try:  # Check if path exists, error if it does not
        assert os.path.exists(path)
    except AssertionError:
        f = open("error.txt", "w")
        f.write(
            "Could not find the path you specified, make sure you input the correct one")
        f.close()
        print("Could not find the path you specified, make sure you input the correct one.")
        input("Press 'Enter' to exit")
        sys.exit()


def read_score(file_path):
    with open(file_path, newline='') as csvfile:
        for row in csv.reader(csvfile):
            if row and row[0] == 'Score:':
                return row[1]
    return '0'


def cells_from_sheet_ranges(ranges):
    valid_range = re.compile(r'(?P<sheet>.+)!(?P<row1>[A-Z]+)(?P<col1>\d+)(:(?P<row2>[A-Z]+)(?P<col2>\d+))?')
    for r in ranges:
        if (m := valid_range.match(r)) and m.group('row1') == m.group('row2'):
            if m.group('col2'):
                for i in range(int(m.group('col1')), int(m.group('col2')) + 1):
                    yield f'{m.group("sheet")}!{m.group("row1")}{i}'
            else:
                yield r
        else:
            f = open("error.txt", "w")
            f.write(
                "Invalid sheet range: " + r
                + "\nIf you are not sure what this means, try looking into the readme.")
            f.close()
            print("Invalid sheet range:")
            print(r)
            print("If you are not sure what this means, try looking into the readme.")
            input("Press 'Enter' to exit")
            sys.exit()


def read_sheet_range(sheet_range):
    try:
        response = (SHEET_API.values()
                             .get(spreadsheetId=SHEET_ID, range=sheet_range)
                             .execute()
                             .get('values', [['0']]))
        flat = [val.strip() for row in response for val in row]
        return flat
    except HttpError as error:
        f = open("error.txt", "w")
        f.write(
            "Sheets API: " + error._get_reason()
            + "\nIf you are not sure what this means, try looking into the readme."
        )
        f.close()
        print("Sheets API: " + error._get_reason()
              + "\nIf you are not sure what this means, try looking into the readme.")
        input("Press 'Enter' to exit")
        sys.exit()


def init_scenario_data():
    hs_cells_iter = cells_from_sheet_ranges(CONFIG['highscore_ranges'])
    avg_cells_iter = cells_from_sheet_ranges(CONFIG['average_ranges'])
    scens = {}

    for r in CONFIG['scenario_name_ranges']:
        for s in read_sheet_range(r):
            if s not in scens:
                scens[s] = {
                    'hs_cells': [],
                    'avg_cells': [],
                    'hs': 0,
                    'avgs': [],
                    'hs_updated': False,
                    'avg_updated': False,
                }

            scens[s]['hs_cells'].append(next(hs_cells_iter))
            scens[s]['avg_cells'].append(next(avg_cells_iter))

    for s in scens:
        for cell in scens[s]['hs_cells']:
            scens[s]['hs'] = max(scens[s]['hs'], float(read_sheet_range(cell)[0]))

    return scens


def update_scenario_data(scens, file_names):
    for f in file_names:
        s = f[0:f.find(" - Challenge - ")]
        if s in scens:
            score = round(float(read_score(f'{CONFIG["path_to_stats"]}/{f}')), 1)
            scen = scens[s]
            if score > scen['hs']:
                scen['hs'] = score
                scen['hs_updated'] = True

            if CONFIG['calculate_averages']:
                scen['avgs'].append(score) # Will be last N runs if files are sorted
                if len(scen['avgs']) > CONFIG['num_of_runs_to_average']:
                    scen['avgs'].pop(0)
                scen['avg_updated'] = True


def update_sheet(scens):
    try:
        for s in scens:
            if scens[s]['hs_updated']:
                for cell in scens[s]['hs_cells']:
                    SHEET_API.values().update(spreadsheetId=SHEET_ID,
                                              range=cell,
                                              valueInputOption='RAW',
                                              body={'values': [[scens[s]['hs']]]}).execute()
                scens[s]['hs_updated'] = False
            if scens[s]['avg_updated']:
                avg = round(sum(scens[s]['avgs']) / len(scens[s]['avgs']), 1)
                for cell in scens[s]['avg_cells']:
                    SHEET_API.values().update(spreadsheetId=SHEET_ID,
                                              range=cell,
                                              valueInputOption='RAW',
                                              body={'values': [[avg]]}).execute()
                scens[s]['avg_updated'] = False
    except HttpError as error:
        f = open("error.txt", "w")
        f.write(
            "Sheets API: " + error._get_reason()
            + "\nIf you are not sure what this means, try looking into the readme."
        )
        f.close()
        print("Sheets API: " + error._get_reason()
              + "\nIf you are not sure what this means, try looking into the readme.")
        input("Press 'Enter' to exit")
        sys.exit()


scenarios = init_scenario_data()

check_stats_path(CONFIG['path_to_stats'])
all_files = [f.lower() for f in list(os.listdir(CONFIG['path_to_stats']))]
all_files.sort()

if CONFIG['update_sheet_on_startup']:
    update_scenario_data(scenarios, all_files)
    update_sheet(scenarios)

while True:
    all_files_updated = os.listdir(CONFIG['path_to_stats'])
    new_files = [file for file in all_files_updated if file not in all_files]
    update_scenario_data(scenarios, new_files)
    consoleOutput.create_output(consoleOutput, scenarios)
    update_sheet(scenarios)
    all_files = all_files_updated
    time.sleep(CONFIG['polling_interval'])