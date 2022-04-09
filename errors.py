import logging
import sys


def handle_error(error_type, val=''):
    logging.error({
                      'average': 'An error occured while calculating averages',
                      'no_credentials': 'Follow the setup steps here: https://github.com/VoltaicHQ/Progress-Sheet-Updater',
                      'range': f'Invalid sheet range: {val}',
                      'range_size': 'Range size mismatched, check that each list of ranges in config.json have the same number of cells referenced.',
                      'sheets_api': f'Sheets API error: {val}',
                      'stats_path': f'Could not find the folder: {val}',
                      'unknown': 'An unknown error occurred.'
                  }.get(error_type, 'unknown'))

    input("Press 'Enter' to exit...")
    sys.exit()
