from get_path import *
from get_spreadsheet import *
from get_output import *
import os
import time

# Global Variables
average_pointers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Points to the index where the new
# score will be added in average tab
benchmark_range_name = 'Benchmarks!F3:F22'
average_range_name = 'Average for benchmarks!D2:H21'
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

bench_spreadsheet_id = sr.read_spreadsheet_id(sr)
sr.check_spreadsheet_id(sr, bench_spreadsheet_id)
service = sr.create_service(sr)

# Check if path to stats folder was already given, if not create it
path = pr.get_path(pr)

# Create a List of all files in the stats folder
all_files = os.listdir(path)

# Create a list with all Benchmarknames
benchmark_names = sr.get_benchmarks(sr)

# Initialize list highscores and connection to benchmark part of sheet
sheet = service.spreadsheets()
result_highscores = sheet.values().get(spreadsheetId=bench_spreadsheet_id, range=benchmark_range_name).execute()
highscores = result_highscores.get("values", [])

# Change values in the lists inside the highscores to float, or sheets will weird out, also insert 0 into empty columns
for score in highscores:
    if not score:
        score.insert(0, "0")
    score[0] = float(score[0])

# Initialize list averages and connection to average part of sheet
result_averages = sheet.values().get(spreadsheetId=bench_spreadsheet_id, range=average_range_name).execute()
averages = result_averages.get("values", [])

# Change values in the lists inside the averages to float, or sheets will spaz out, also insert "" into empty lists
while len(averages) < 20:
    averages.insert(len(averages), [])
for average in averages:
    while len(average) < 5:
        average.insert(len(average), "")
    for score in average:
        if score != "":
            average[average.index(score)] = float(score)

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
                            averages[index_bench][pointerposition] = current
                            if current > benchmark_score:  # If new Score > Highscore
                                highscores[benchmark_names.index(bench)][0] = current  # Update highscore of the bench
                                found = True

        if bench_played:  # If a Bench was played update the average tab on the Googlesheet
            valuesavg = [
                averages[0],
                averages[1],
                averages[2],
                averages[3],
                averages[4],
                averages[5],
                averages[6],
                averages[7],
                averages[8],
                averages[9],
                averages[10],
                averages[11],
                averages[12],
                averages[13],
                averages[14],
                averages[15],
                averages[16],
                averages[17],
                averages[18],
                averages[19],
            ]
            bodyavg = {
                'values': valuesavg
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=bench_spreadsheet_id, range=average_range_name,
                valueInputOption="RAW", body=bodyavg).execute()  # Send request to API, update the average tab

        if found:  # If a new Highscore was found update the value on the Google Sheet
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
                highscores[18],
                highscores[19],
            ]
            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=bench_spreadsheet_id, range=benchmark_range_name,
                valueInputOption="RAW", body=body).execute()  # Send request to API, update benchmark tab
        cls()
        op.create_output(op, found, benchmark_names, changed_bench_index, current, bench_played, averages)
        all_files = all_files_updated  # Update the value of allfiles, so that you dont compare the same new scores
        time.sleep(60)  # Wait 60 Seconds until next check
except KeyboardInterrupt:
    print("Exiting...")
    pass
