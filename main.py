from get_path import *
from get_spreadsheet import *
from get_output import *
import os
import time

# Global Variables
average_pointers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Points to the index where the new score will be added in average tab
INTERMEDIATE_SCORE_RANGE = 'Intermediate Requirements!G3:G20'
ADVANCED_SCORE_RANGE = 'Advanced Requirements!G3:G20'
INTERMEDIATE_AVERAGE_RANGE = 'Intermediate Requirements!M3:M20'
ADVANCED_AVERAGE_RANGE = 'Advanced Requirements!M3:M20'
INTERMEDIATE_NAME_RANGE = 'Intermediate Requirements!E3:E20'
ADVANCED_NAME_RANGE = 'Advanced Requirements!E3:E20'

# Objects from the imported classes
sr = spreadSheetReader
pr = pathReader
op = consoleOutput


# Functions
# Function to clear console window
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Function to move the pointer of the played benchmark
def movepointer(index_played_bench):
    oldpointer = average_pointers[index_played_bench]  # Backup old pointer position to return later
    currentpointer = average_pointers[index_played_bench]
    if currentpointer != 4:  # If the pointer is not on the last column, move to one column ahead
        currentpointer = currentpointer + 1
    elif currentpointer == 4:  # If pointer is on the last column, go back to first column
        currentpointer = 0
    average_pointers[index_played_bench] = currentpointer  # Update pointer in array
    return oldpointer


# Create GoogleAPI Service
BENCH_SPREADSHEET_ID = sr.read_spreadsheet_id(sr)
sr.check_spreadsheet_id(sr, BENCH_SPREADSHEET_ID)
service = sr.create_service(sr)
sheet = service.spreadsheets()
# Check if path to stats folder was already given, if not create it
path = pr.get_path(pr)

# Create a List of all files in the stats folder
all_files = os.listdir(path)

# Create a list with all Benchmarknames
result_names_intermediate = sheet.values().get(spreadsheetId=BENCH_SPREADSHEET_ID,
                                               range=INTERMEDIATE_NAME_RANGE).execute()
result_names_advanced = sheet.values().get(spreadsheetId=BENCH_SPREADSHEET_ID,
                                           range=ADVANCED_NAME_RANGE).execute()
names_intermediate = []
names_intermediate = result_names_intermediate.get("values", [])
names_advanced = result_names_advanced.get("values", [])

benchmark_names = names_intermediate + names_advanced
del benchmark_names[21:24]

i = 0
while i < len(benchmark_names):
    benchmark_names[i] = benchmark_names[i][0].strip()
    i += 1
# Initialize both lists for highscores and connection to benchmark part of sheet

result_highscores_intermediate = sheet.values().get(spreadsheetId=BENCH_SPREADSHEET_ID,
                                                    range=INTERMEDIATE_SCORE_RANGE).execute()
result_highscores_advanced = sheet.values().get(spreadsheetId=BENCH_SPREADSHEET_ID,
                                                range=ADVANCED_SCORE_RANGE).execute()
highscores_intermediate = result_highscores_intermediate.get("values", [])
highscores_advanced = result_highscores_advanced.get("values", [])
# Change values in the lists inside the highscores to float, or sheets will weird out, also insert 0 into empty columns
while len(highscores_intermediate) < 18:
    highscores_intermediate.append([0])

while len(highscores_advanced) < 18:
    highscores_advanced.append([0])

for score in highscores_intermediate:
    if not score:
        score.insert(0, "0")
    score[0] = float(score[0])

for score in highscores_advanced:
    if not score:
        score.insert(0, "0")
    score[0] = float(score[0])

#  Create a list with all scores, then remove the ones that are duplicats
highscores = highscores_intermediate + highscores_advanced
del highscores[21:24]

# Initialize lists for averages and connection to average part of sheet
result_averages_intermediate = sheet.values().get(spreadsheetId=BENCH_SPREADSHEET_ID,
                                                  range=INTERMEDIATE_AVERAGE_RANGE).execute()
result_averages_advanced = sheet.values().get(spreadsheetId=BENCH_SPREADSHEET_ID,
                                                  range=ADVANCED_AVERAGE_RANGE).execute()
averages_intermediate = result_averages_intermediate.get("values", [])
averages_advanced = result_averages_advanced.get("values", [])

# Change values in the average lists to float, or sheets will spaz out, also insert 0 into empty cells
while len(averages_intermediate) < 18:
    averages_intermediate.append([0])

while len(averages_advanced) < 18:
    averages_advanced.append([0])

for score in averages_intermediate:
    if not score:
        score.insert(0, "0")
    score[0] = float(score[0])

for score in averages_advanced:
    if not score:
        score.insert(0, "0")
    score[0] = float(score[0])

calculated_averages = averages_intermediate + averages_advanced
del calculated_averages[21:24]

averages = []
for score in calculated_averages:
    averages.append([score]*5)

# Run a while that stops on Ctrl+C press
try:
    while True:
        changed_bench_index = None
        current = None
        found = False  # Boolean False to check if a new highscore was found
        bench_played = False  # Boolean False to check if a bench was played
        all_files_updated = os.listdir(path)
        # Create a list (new_entries) of all files that were created since the last time the loop ran
        s = set(all_files)
        new_entries = [x for x in all_files_updated if x not in s]
        for entry in new_entries:
            entryname = entry[0:entry.find(" - Challenge - ")]  # Extract Name of Bench from the filename
            for bench in benchmark_names:  # Compare names of scens that were last played to the Benchmark names
                index_bench = benchmark_names.index(bench)
                benchmark_score = float(highscores[index_bench][0])
                if bench.lower() == entryname.lower():  # If a benchmark scenario was recently played
                    changed_bench_index = index_bench
                    bench_played = True
                    f = open(path + "\\" + entry, "r")  # Open file and read the Score achieved in it
                    content = f.read()
                    f.close()
                    seperatedlines = content.splitlines()
                    for line in seperatedlines:
                        if line.find("Score") != -1:
                            current = float(line[7:])
                            current = round(current, 1)
                            pointerposition = movepointer(index_bench)
                            averages[index_bench][pointerposition] = [current]
                            if current > benchmark_score:  # If new Score > Highscore
                                highscores[benchmark_names.index(bench)][0] = current  # Update highscore of the bench
                                found = True
                            break
        print(changed_bench_index)

        if bench_played:  # If a Bench was played update the average tab on the Googlesheet
            calculated_averages[changed_bench_index] = [op.get_average(op, averages, changed_bench_index)]
            if changed_bench_index < 17:  # If the changed score is on the intermediate tab

                valuesavg = [
                    calculated_averages[0],
                    calculated_averages[1],
                    calculated_averages[2],
                    calculated_averages[3],
                    calculated_averages[4],
                    calculated_averages[5],
                    calculated_averages[6],
                    calculated_averages[7],
                    calculated_averages[8],
                    calculated_averages[9],
                    calculated_averages[10],
                    calculated_averages[11],
                    calculated_averages[12],
                    calculated_averages[13],
                    calculated_averages[14],
                    calculated_averages[15],
                    calculated_averages[16],
                    calculated_averages[17],
                ]
                bodyavg = {
                    'values': valuesavg
                }
                # Send request to API, update the average tab
                result = service.spreadsheets().values().update(spreadsheetId=BENCH_SPREADSHEET_ID,
                                                                range=INTERMEDIATE_AVERAGE_RANGE,
                                                                valueInputOption="RAW",
                                                                body=bodyavg).execute()
            if changed_bench_index > 17 or changed_bench_index == 3 or changed_bench_index == 4 or changed_bench_index == 5:
                values = [
                    calculated_averages[18],
                    calculated_averages[19],
                    calculated_averages[20],
                    calculated_averages[3],
                    calculated_averages[4],
                    calculated_averages[5],
                    calculated_averages[21],
                    calculated_averages[22],
                    calculated_averages[23],
                    calculated_averages[24],
                    calculated_averages[25],
                    calculated_averages[26],
                    calculated_averages[27],
                    calculated_averages[28],
                    calculated_averages[29],
                    calculated_averages[30],
                    calculated_averages[31],
                    calculated_averages[32],
                    ]
                body = {
                    'values': values
                }
                # Send request to API, update benchmark tab
                result = service.spreadsheets().values().update(
                    spreadsheetId=BENCH_SPREADSHEET_ID, range=ADVANCED_AVERAGE_RANGE,
                    valueInputOption="RAW", body=body).execute()

        if found:  # If a new Highscore was found update the value on the Google Sheet
            if changed_bench_index < 17:  # If the changed score is on the intermediate tab
                values = [
                    highscores[0],
                    highscores[1],
                    highscores[2],
                    highscores[3],
                    highscores[4],
                    highscores[5],
                    highscores[6],
                    highscores[7],
                    highscores[8],
                    highscores[9],
                    highscores[10],
                    highscores[11],
                    highscores[12],
                    highscores[13],
                    highscores[14],
                    highscores[15],
                    highscores[16],
                    highscores[17],
                ]
                body = {
                    'values': values
                }
                result = service.spreadsheets().values().update(
                    spreadsheetId=BENCH_SPREADSHEET_ID, range=INTERMEDIATE_SCORE_RANGE,
                    valueInputOption="RAW", body=body).execute()  # Send request to API, update benchmark tab

            if changed_bench_index > 17 or changed_bench_index == 3 or changed_bench_index == 4 or changed_bench_index == 5:
                values = [
                    highscores[18],
                    highscores[19],
                    highscores[20],
                    highscores[3],
                    highscores[4],
                    highscores[5],
                    highscores[22],
                    highscores[23],
                    highscores[23],
                    highscores[24],
                    highscores[25],
                    highscores[26],
                    highscores[27],
                    highscores[28],
                    highscores[29],
                    highscores[30],
                    highscores[31],
                    highscores[32],
                    ]
                body = {
                    'values': values
                }
                result = service.spreadsheets().values().update(
                    spreadsheetId=BENCH_SPREADSHEET_ID, range=ADVANCED_SCORE_RANGE,
                    valueInputOption="RAW", body=body).execute()  # Send request to API, update benchmark tab

        cls()
        op.create_output(op, found, benchmark_names, changed_bench_index, current, bench_played, averages)
        all_files = all_files_updated  # Update the value of allfiles, so that you dont compare the same new scores
        time.sleep(60)  # Wait 60 Seconds until next check
except KeyboardInterrupt:
    print("Exiting...")
    pass
