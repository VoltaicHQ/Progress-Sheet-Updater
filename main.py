import csv
import json
import logging
import logging.config
import os
import sqlite3
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from threading import Timer

import googleapiclient.discovery
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from errors import handle_error
from gui import Gui
from sheets import create_service, read_sheet_range, validate_sheet_range, write_to_cell
from conf import AIMLAB_DB_PATH


@dataclass
class Scenario:
    hs_cells: list = field(default_factory=list)
    avg_cells: list = field(default_factory=list)
    hs: float = 0
    avg: float = 0
    recent_scores: list = field(default_factory=list)
    ids: list = field(default_factory=list)


def cells_from_sheet_ranges(ranges: str):
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


def init_scenario_data_kovaaks(config: dict, sheet_api: googleapiclient.discovery.Resource) -> dict:
    hs_cells_iter = cells_from_sheet_ranges(config['highscore_ranges'])
    if config["calculate_averages"]:
        avg_cells_iter = cells_from_sheet_ranges(config['average_ranges'])

    scens = {}

    i = 0
    for r in config['scenario_name_ranges']:
        for s in read_sheet_range(sheet_api, config["sheet_id_kovaaks"], r):
            if s not in scens:
                scens[s] = Scenario()

            scens[s].hs_cells.append(next(hs_cells_iter))
            if config["calculate_averages"]:
                try:
                    scens[s].avg_cells.append(next(avg_cells_iter))
                except AttributeError as err:
                    handle_error("averages")
            scens[s].ids.append(i)
            i += 1

    highscores = []
    for r in config['highscore_ranges']:
        highscores += map(lambda x: float(x), read_sheet_range(sheet_api, config["sheet_id_kovaaks"], r))

    if config["calculate_averages"]:
        averages = []
        for r in config['average_ranges']:
            averages += map(lambda x: float(x), read_sheet_range(sheet_api, config["sheet_id_kovaaks"], r))

    if len(highscores) < len(scens):  # Require highscore cells but not averages
        handle_error('range_size')

    for s in scens:
        scens[s].hs = min([highscores[i] for i in scens[s].ids])
        if config["calculate_averages"]:
            scens[s].avg = min([averages[i] for i in scens[s].ids])

    return scens


def init_scenario_data_aimlab(config: dict, sheet_api: googleapiclient.discovery.Resource) -> dict:
    hs_cells_iter = cells_from_sheet_ranges(config['aimlab_score_ranges'])
    avg_cells_iter = cells_from_sheet_ranges(config['aimlab_average_ranges'])

    scens = {}

    i = 0
    for r in config['aimlab_name_ranges']:
        for s in read_sheet_range(sheet_api, config["sheet_id_aimlab"], r):
            if s not in scens:
                scens[s] = Scenario()

            scens[s].hs_cells.append(next(hs_cells_iter))
            scens[s].avg_cells.append(next(avg_cells_iter))
            scens[s].ids.append(i)
            i += 1

    highscores = []
    for r in config['aimlab_score_ranges']:
        highscores += map(lambda x: float(x), read_sheet_range(sheet_api, config["sheet_id_aimlab"], r))

    averages = []
    for r in config['aimlab_average_ranges']:
        averages += map(lambda x: float(x), read_sheet_range(sheet_api, config["sheet_id_aimlab"], r))

    if len(highscores) < len(scens):  # Require highscore cells but not averages
        handle_error('range_size')

    for s in scens:
        scens[s].hs = min([highscores[i] for i in scens[s].ids])
        scens[s].avg = min([averages[i] for i in scens[s].ids])

    return scens


def read_score_from_file(file_path: str) -> float:
    with open(file_path, newline='') as csvfile:
        for row in csv.reader(csvfile):
            if row and row[0] == 'Score:':
                return round(float(row[1]), 1)
    return 0.0


def update_aimlab(config: dict, scens: dict, cs_level_ids: dict, blacklist: dict) -> None:
    new_hs = set()
    new_avgs = set()

    # Open db connection
    con = sqlite3.connect(AIMLAB_DB_PATH)
    cur = con.cursor()

    # Get scores from the database
    result = []
    for csid, name in cs_level_ids.items():
        cur.execute(
            f"SELECT taskName, score FROM TaskData WHERE taskName = ? AND createDate > date(?)",
            [csid, blacklist[name]])
        temp = cur.fetchall()
        result.extend(temp)

    for s in result:
        name = cs_level_ids[s[0]]
        score = s[1]
        if score > scens[name].hs:
            scens[name].hs = score
            new_hs.add(name)

        if config['calculate_averages']:
            scens[name].recent_scores.append(score)  # Will be last N runs if files are fed chronologically
            if len(scens[name].recent_scores) > config['num_of_runs_to_average']:
                scens[name].recent_scores.pop(0)

    if config['calculate_averages']:
        for s in scens:
            runs = scens[s].recent_scores
            if runs:  # If the scenario was never played this would result in a div by zero error
                new_avg = round(sum(runs) / len(runs), 1)
            if runs and new_avg != scens[s].avg:
                scens[s].avg = new_avg
                new_avgs.add(s)

    create_output(new_hs, new_avgs, scens, config["sheet_id_aimlab"])  # check averages here as well


def update_kovaaks(config: dict, scens: dict, files: list, blacklist: dict) -> None:
    new_hs = set()
    new_avgs = set()

    # Process new runs to populate new_hs and new_avgs
    for f in files:
        s = f[0:f.find(" - Challenge - ")].lower().strip()
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
            if runs:  # If the scenario was never played this would result in a div by zero error
                new_avg = round(sum(runs) / len(runs), 1)
            if runs and new_avg != scens[s].avg:
                scens[s].avg = new_avg
                new_avgs.add(s)

    create_output(new_hs, new_avgs, scens, config["sheet_id_kovaaks"])


def create_output(new_hs: dict, new_avgs: dict, scens: dict, sheet_id: str) -> None:
    # Pretty output and update progress sheet
    if not new_hs and not new_avgs:
        logging.info('Your progress sheet is up-to-date.')
        return

    if new_hs:
        logging.info(f'New Highscore{"s" if len(new_hs) > 1 else ""}')
        for s in new_hs:
            logging.info(f'{scens[s].hs:>10} - {s}')
            for cell in scens[s].hs_cells:
                write_to_cell(sheet_api, sheet_id, cell, scens[s].hs)

    if new_avgs:
        logging.info(f' New Average{"s" if len(new_hs) > 1 else ""}')
        for s in new_avgs:
            logging.info(f'{scens[s].avg:>10} - {s}')
            for cell in scens[s].avg_cells:
                write_to_cell(sheet_api, sheet_id, cell, scens[s].avg)


def init_version_blacklist() -> dict:
    url = 'https://docs.google.com/spreadsheets/d/1uvXfx-wDsyPg5gM79NDTszFk-t6SL42seL-8dwDTJxw/gviz/tq?tqx=out:csv&sheet=Update_Dates'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    blacklist = dict()
    for line in lines[1:]:
        splits = line.split('","')
        name = splits[0].replace('"', '')
        date = datetime.strptime(splits[1].replace('"', '').replace('\n', ''), "%d.%m.%Y").date()
        blacklist[name.lower()] = date

    return blacklist


def init_cs_level_ids_and_blacklist() -> (dict, dict):
    url = 'https://docs.google.com/spreadsheets/d/1uvXfx-wDsyPg5gM79NDTszFk-t6SL42seL-8dwDTJxw/gviz/tq?tqx=out:csv&sheet=cslevelids'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cs_level_ids = dict()
    blacklist = dict()
    for line in lines[1:]:
        splits = line.split('","')
        name = splits[0].replace('"', '')
        cs_level_id = splits[1].replace('"', '')
        cs_level_ids[cs_level_id] = name.lower()
        date = datetime.strptime(splits[2].replace('"', '').replace('\n', ''), "%d.%m.%Y").date()
        blacklist[name.lower()] = date

    return cs_level_ids, blacklist


class LambdaDispatchEventHandler(FileSystemEventHandler):

    def __init__(self, func):
        self.func = func

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            if config["game"] == "Kovaaks" or event.src_path.endswith("klutch.bytes"):
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


@debounce(5)
def process_files_kovaaks():
    global config, sheet_api, blacklist, scenarios, stats

    new_stats = os.listdir(config['stats_path'])
    unprocessed = list(sorted([f for f in new_stats if f not in stats]))
    update_kovaaks(config, scenarios, unprocessed, blacklist)
    stats = new_stats


@debounce(5)
def process_files_aimlab():
    global config, sheet_api, scenarios, cs_level_ids, blacklist

    update_aimlab(config, scenarios, cs_level_ids, blacklist)


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Function that replaces sys.excepthook to also log uncaught exceptions, see:
    https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python/16993115#16993115
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    sys.excepthook = handle_exception

    config_file = 'config.json'
    if not os.path.isfile(config_file):
        logging.error("Failed to find config file: %s", config_file)
        sys.exit(1)

    config = json.load(open(config_file, 'r'))
    gui = Gui(**config)
    gui.main()

    try:
        config = json.load(open(config_file, 'r'))
        logging.debug(json.dumps(config, indent=2))
    except Exception as err:
        logging.debug(json.dumps(config, indent=2))
        handle_error('no_credentials')

    logging.debug("Creating service...")
    sheet_api = create_service()

    # Aimlab has its data in /AppData/LocalLow/statespace/aimlab_tb/klutch.bytes
    if config["game"] == "Aimlab":
        logging.debug("Game: Aimlab")
        logging.debug("Initializing scenario data...")
        scenarios = init_scenario_data_aimlab(config, sheet_api)
        logging.debug("Initializing CsLevelIds...")
        cs_level_ids, blacklist = init_cs_level_ids_and_blacklist()
        update_aimlab(config, scenarios, cs_level_ids, blacklist)

    # Kovaaks has its data in the stats folder
    elif config["game"] == "Kovaaks":
        logging.debug("Game: Kovaaks")
        logging.debug("Initializing scenario data...")
        scenarios = init_scenario_data_kovaaks(config, sheet_api)
        logging.debug("Initializing version blacklist...")
        blacklist = init_version_blacklist()

        stats = list(sorted(os.listdir(config['stats_path'])))

        update_kovaaks(config, scenarios, stats, blacklist)

    if config['run_mode'] == 'once':
        logging.info("Finished Updating, program will close in 3 seconds...")
        time.sleep(3)
        sys.exit()
    elif config['run_mode'] == 'watchdog':
        observer = Observer()
        if config["game"] == "Kovaaks":
            event_handler = LambdaDispatchEventHandler(lambda: process_files_kovaaks())
            observer.schedule(event_handler, config['stats_path'])
        elif config["game"] == "Aimlab":
            event_handler = LambdaDispatchEventHandler(lambda: process_files_aimlab())
            observer.schedule(event_handler, os.path.join(AIMLAB_DB_PATH, os.pardir))
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    elif config['run_mode'] == 'interval':
        while True:
            if config["game"] == "Kovaaks":
                process_files_kovaaks()
            elif config["game"] == "Aimlab":
                process_files_aimlab()
            try:
                time.sleep(max(config['polling_interval'], 30))
            except KeyboardInterrupt:
                logging.debug('Received keyboard interrupt.')
                break
    else:
        logging.info("Run mode is not supported. Supported types are 'once'/'watchdog'/'interval'.")

    logging.info("Program will close in 3 seconds...")
    time.sleep(3)
    sys.exit()
