import sys

def handle_error(error_type, error=None, val=''):
    print({
        'no_credentials': 'Could not find your credentials file, place it in the same folder as this executable.',
        'range': f'Invalid sheet range: {val}',
        'range_size': 'Range size mismatched, check that each list of ranges in config.json have the same number of cells referenced.',
        'sheets_api': f'Sheets API error: {error._get_reason()}',
        'stats_path': f'Could not find the folder: {val}',
        'unknown': 'An unknown error occured.'
    }).get(error_type, 'unknown')
    
    input("Press any key to exit...")
    sys.exit()