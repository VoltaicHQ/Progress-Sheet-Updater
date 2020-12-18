import sys
import os
import time
import json
import csv
from scenario import Scenario
from sheets import cells_from_sheet_ranges, read_sheet_range, write_to_cell, create_service
from errors import handle_error
from typing import List
from datetime import datetime


def init_scenario_data(config, sheet_api):
    hs_cells_iter = cells_from_sheet_ranges(config['highscore_ranges'])
    avg_cells_iter = cells_from_sheet_ranges(config['average_ranges'])

    scens = {}

    i = 0
    for r in config['scenario_name_ranges']:
        for s in read_sheet_range(sheet_api, config['sheet_id'], r):
            if s not in scens:
                scens[s] = Scenario()

            scens[s].hs_cells.append(next(hs_cells_iter))
            scens[s].avg_cells.append(next(avg_cells_iter))
            scens[s].ids.append(i)
            i += 1

    highscores = []
    for r in config['highscore_ranges']:
        highscores += map(lambda x: float(x), read_sheet_range(sheet_api, config['sheet_id'], r))

    averages = []
    for r in config['average_ranges']:
        averages += map(lambda x: float(x), read_sheet_range(sheet_api, config['sheet_id'], r))

    if len(highscores) < len(scens): # Require highscore cells but not averages
        handle_error('range_too_small')

    for s in scens:
        scens[s].hs = max([highscores[i] for i in scens[s].ids])
        scens[s].avg = max([averages[i] for i in scens[s].ids])

    return scens
    

def read_score_from_file(file_path):
    with open(file_path, newline='') as csvfile:
        for row in csv.reader(csvfile):
            if row and row[0] == 'Score:':
                return round(float(row[1]), 1)
    return 0.0


def update(config, scens, files):
    new_hs = []
    new_avgs = []

    # Process new runs to populate new_hs and new_avgs
    for f in files:
        s = f[0:f.find(" - Challenge - ")]
        if s in scens:
            score = read_score_from_file(f'{config["stats_path"]}/{f}')

            if score > scens[s].hs:
                scens[s].hs = score
                new_hs.append(s)

            if config['calculate_averages']:
                scens[s].recent_scores.append(score) # Will be last N runs if files are fed chronologically
                if len(scens[s].recent_scores) > config['num_of_runs_to_average']:
                    scens[s].recent_scores.pop(0)
    
    if config['calculate_averages']:
        for s in scens:
            runs = scens[s].recent_scores
            if runs and (new_avg := round(sum(runs) / len(runs), 1)) != scens[s].avg:
                scens[s].avg = new_avg
                new_avgs.append(s)

    # Pretty output and update progress sheet
    time = datetime.now()

    if not new_hs and not new_avgs:
        print(f'[{time:%H:%M:%S}] Your progress sheet is up-to-date')
        return

    if new_hs:
        print(f'[{time:%H:%M:%S}] New Highscores')
        for s in new_hs:
            print(f'{scens[s].hs:>10} - {s}')
            for cell in scens[s].hs_cells:
                write_to_cell(sheet_api, config['sheet_id'], cell, scens[s].hs)
    
    if new_avgs:
        print(f'[{time:%H:%M:%S}] New Averages')
        for s in new_avgs:
            print(f'{scens[s].avg:>10} - {s}')
            for cell in scens[s].avg_cells:
                write_to_cell(sheet_api, config['sheet_id'], cell, scens[s].avg)
    

config = json.load(open('config.json', 'r'))
sheet_api = create_service()
scenarios = init_scenario_data(config, sheet_api)
stats = list(sorted(os.listdir(config['stats_path'])))

if config['update_sheet_on_startup']:
    update(config, scenarios, stats)
    time.sleep(config['polling_interval'])

while True:
    new_stats = os.listdir(config['stats_path'])
    unprocessed = list(sorted([f for f in new_stats if f not in stats]))
    update(config, scenarios, unprocessed)
    stats = new_stats
    time.sleep(config['polling_interval'])