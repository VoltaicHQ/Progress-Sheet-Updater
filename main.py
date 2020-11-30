from get_spreadsheet import spreadSheetReader
from get_output import consoleOutput
from util import avg, handle_error
import sys
import os
import time
import json
import re
import csv
from googleapiclient.errors import HttpError

CONFIG = json.load(open("config.json", "r"))
SHEET_API = spreadSheetReader.create_service(spreadSheetReader).spreadsheets()
SHEET_ID = spreadSheetReader.read_spreadsheet_id(spreadSheetReader, CONFIG['link_to_sheet'])


def check_stats_path(path):
    try:  # Check if path exists, error if it does not
        assert os.path.exists(path)
    except AssertionError:
        handle_error("path")


def read_score(file_path):
    with open(file_path, newline='') as csvfile:
        for row in csv.reader(csvfile):
            if row and row[0] == 'Score:':
                return round(float(row[1]), 1)
    return 0.0


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
            handle_error("range", r=r)


def read_sheet_range(sheet_range):
    try:
        response = (SHEET_API.values()
                             .get(spreadsheetId=SHEET_ID, range=sheet_range)
                             .execute()
                             .get('values', [['0']]))
        flat = [val.strip() for row in response for val in row]
        return flat
    except HttpError as error:
        handle_error("api", error=error)


def init_scenario_data():
    hs_cells_iter = cells_from_sheet_ranges(CONFIG['highscore_ranges'])
    avg_cells_iter = cells_from_sheet_ranges(CONFIG['average_ranges'])
    scens = {}

    i = 0
    j = 0
    for r in CONFIG['scenario_name_ranges']:
        for s in read_sheet_range(r):
            if s not in scens:
                scens[s] = {
                    'hs_cells': [],
                    'avg_cells': [],
                    'hs': 0,
                    'avg': 0,
                    'runs': [],
                    'hs_updated': False,
                    'avg_updated': False,
                    'hs_ids': [],
                    'avg_ids': []
                }

            scens[s]['hs_cells'].append(next(hs_cells_iter))
            scens[s]['avg_cells'].append(next(avg_cells_iter))
            scens[s]['hs_ids'].append(i)
            scens[s]['avg_ids'].append(j)
            i += 1
            j += 1

    highscores = []
    for r in CONFIG['highscore_ranges']:
        highscores += map(lambda x: float(x), read_sheet_range(r))

    averages = []
    for r in CONFIG['average_ranges']:
        averages += map(lambda x: float(x), read_sheet_range(r))

    if len(highscores) < len(scens): # Require highscores but not averages
        handle_error('range_too_small')

    for s in scens:
        for i in scens[s]['hs_ids']:
            scens[s]['hs'] = max(scens[s]['hs'], highscores[i])
        for j in scens[s]['avg_ids']:
            scens[s]['avg'] = max(scens[s]['avg'], averages[j])

    return scens


def update_scenario_data(scens, file_names):
    for f in file_names:
        s = f[0:f.find(" - Challenge - ")]
        if s in scens:
            score = read_score(f'{CONFIG["path_to_stats"]}/{f}')

            if score > scens[s]['hs']:
                scens[s]['hs'] = score
                scens[s]['hs_updated'] = True

            if CONFIG['calculate_averages']:
                scens[s]['runs'].append(score) # Will be last N runs if files are sorted
                if len(scens[s]['runs']) > CONFIG['num_of_runs_to_average']:
                    scens[s]['runs'].pop(0)

    for s in scens:
        if (new_avg := avg(scens[s]['runs'])) != scens[s]['avg']:
            print(f'{s} {scens[s]["runs"]}  {scens[s]["avg"]} -> {new_avg}')
            scens[s]['avg'] = new_avg
            scens[s]['avg_updated'] = True

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
                for cell in scens[s]['avg_cells']:
                    SHEET_API.values().update(spreadsheetId=SHEET_ID,
                                              range=cell,
                                              valueInputOption='RAW',
                                              body={'values': [[scens[s]['avg']]]}).execute()
                scens[s]['avg_updated'] = False
    except HttpError as error:
        handle_error("api", error=error)


scenarios = init_scenario_data()

check_stats_path(CONFIG['path_to_stats'])
all_files = list(os.listdir(CONFIG['path_to_stats']))
all_files.sort()

if CONFIG['update_sheet_on_startup']:
    update_scenario_data(scenarios, all_files)
    update_sheet(scenarios)

try:
    while True:
        all_files_updated = os.listdir(CONFIG['path_to_stats'])
        new_files = [file for file in all_files_updated if file not in all_files]
        update_scenario_data(scenarios, new_files)
        consoleOutput.create_output(consoleOutput, scenarios)
        update_sheet(scenarios)
        all_files = all_files_updated
        time.sleep(CONFIG['polling_interval'])
except KeyboardInterrupt:
    print("Exiting...")
    pass