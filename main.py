import csv
import json
import os
import urllib.request
import time
from dataclasses import dataclass, field
from datetime import datetime
from threading import Timer
from watchdog.events import FileSystemEventHandler
from errors import handle_error
from sheets import create_service, read_sheet_range, validate_sheet_range, write_to_cell
import sys
from watchdog.observers import Observer


@dataclass
class Scenario:
    hs_cells: list = field(default_factory=list)
    avg_cells: list = field(default_factory=list)
    hs: float = 0
    avg: float = 0
    recent_scores: list = field(default_factory=list)
    ids: list = field(default_factory=list)


def cells_from_sheet_ranges(ranges):
    for r in ranges:
        m = validate_sheet_range(r)
        if m.group('col1') == m.group('col2'):
            if m.group('row2'):
                for i in range(int(m.group('row1')), int(m.group('row2')) + 1):
                    yield f'{m.group("sheet")}!{m.group("col1")}{i}'
            else:
                yield r
        else:
            handle_error('range', val=r)


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

    if len(highscores) < len(scens):  # Require highscore cells but not averages
        handle_error('range_size')

    for s in scens:
        scens[s].hs = min([highscores[i] for i in scens[s].ids])
        scens[s].avg = min([averages[i] for i in scens[s].ids])

    return scens


def read_score_from_file(file_path):
    with open(file_path, newline='') as csvfile:
        for row in csv.reader(csvfile):
            if row and row[0] == 'Score:':
                return round(float(row[1]), 1)
    return 0.0


def update(config, scens, files, blacklist):
    new_hs = set()
    new_avgs = set()

    # Process new runs to populate new_hs and new_avgs
    for f in files:
        s = f[0:f.find(" - Challenge - ")].lower()
        if s in scens:
            if s in blacklist.keys():
                date = f[f.find(" - Challenge - ") + 15:]
                date = date[:date.find("-")]
                playdate = datetime.strptime(date, "%Y.%m.%d").date()
                if playdate <= blacklist[s]:
                    continue
            score = read_score_from_file(f'{config["stats_path"]}/{f}')
            if score > scens[s].hs:
                scens[s].hs = score
                new_hs.add(s)

            if config['calculate_averages']:
                scens[s].recent_scores.append(score)  # Will be last N runs if files are fed chronologically
                if len(scens[s].recent_scores) > config['num_of_runs_to_average']:
                    scens[s].recent_scores.pop(0)

    if config['calculate_averages']:
        for s in scens:
            runs = scens[s].recent_scores
            if runs and (new_avg := round(sum(runs) / len(runs), 1)) != scens[s].avg:
                scens[s].avg = new_avg
                new_avgs.add(s)

    # Pretty output and update progress sheet
    time = datetime.now()

    if not new_hs and not new_avgs:
        print(f'[{time:%H:%M:%S}] Your progress sheet is up-to-date')
        return

    if new_hs:
        print(f'[{time:%H:%M:%S}] New Highscore{"s" if len(new_hs) > 1 else ""}')
        for s in new_hs:
            print(f'{scens[s].hs:>10} - {s}')
            for cell in scens[s].hs_cells:
                write_to_cell(sheet_api, config['sheet_id'], cell, scens[s].hs)

    if new_avgs:
        print(f'[{time:%H:%M:%S}] New Average{"s" if len(new_hs) > 1 else ""}')
        for s in new_avgs:
            print(f'{scens[s].avg:>10} - {s}')
            for cell in scens[s].avg_cells:
                write_to_cell(sheet_api, config['sheet_id'], cell, scens[s].avg)


def init_versionblacklist():
    url = 'https://docs.google.com/spreadsheets/d/1bwub3mY1S58hWsEVzcsuKgDxpCf-3BMXegDa_9cqv0A/gviz/tq?tqx=out:csv&sheet=Update_Dates'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    names = []
    dates = []
    blacklist = dict()
    for l in lines[2:]:
        splits = l.split('","')
        names.append(splits[0].replace('"', ''))
        dates.append(datetime.strptime(splits[1].replace('"', '').replace('\n', ''), "%d.%m.%Y").date())

    for name in names:
        for date in dates:
            blacklist[name.lower()] = date
    return blacklist


class LambdaDispatchEventHandler(FileSystemEventHandler):

    def __init__(self, func):
        self.func = func

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            self.func()


def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked.
        https://gist.github.com/walkermatt/2871026 """

    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)

            try:
                debounced.t.cancel()
            except AttributeError:
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()

        return debounced

    return decorator


config = json.load(open('config.json', 'r'))
sheet_api = create_service()
blacklist = init_versionblacklist()
scenarios = init_scenario_data(config, sheet_api)
stats = list(sorted(os.listdir(config['stats_path'])))


@debounce(5)
def process_files():
    global config, sheet_api, blacklist, scenarios, stats

    new_stats = os.listdir(config['stats_path'])
    unprocessed = list(sorted([f for f in new_stats if f not in stats]))
    update(config, scenarios, unprocessed, blacklist)
    stats = new_stats


update(config, scenarios, stats, blacklist)

if config['run_once']:
    print("Flag run_once is active.")
    print("Finished Updating, program will close in 3 seconds...")
    time.sleep(3)
    sys.exit()

if config['file_watcher_mode'] == 'watchdog':
    event_handler = LambdaDispatchEventHandler(lambda: process_files())
    observer = Observer()
    observer.schedule(event_handler, config['stats_path'])
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
elif config['file_watcher_mode'] == 'interval':
    while True:
        process_files()
        time.sleep(max(config['polling_interval'], 30))
else:
    print("File watcher mode is not supported. Supported types are 'watchdog'/'interval'.")
    print("Finished Updating, program will close in 3 seconds...")
