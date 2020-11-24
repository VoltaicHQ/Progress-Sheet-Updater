from colorama import Fore
from datetime import datetime


# This class handles creating the GoogleAPI Service and fetching the benchmark list
class consoleOutput:
    # Method to get the average from the averages list
    def get_average(self, averages, changed_bench_index):
        # Calculate the average of the changed benchmark
        average = 0.0
        count = 0
        #  Since some scores might be empty we only count the ones that are not
        for score in averages[changed_bench_index]:
            if float(score[0]) != 0.0:
                average = average + float(score[0])
                count += 1
        average = average / count
        average = round(average, 1)
        return average

    # Create console output, vary depending on if a benchmark was played and if a highscore was found
    def create_output(self, highscore_found, benchmark_names, changed_bench_index, current, bench_played, averages):
        print("Progress Sheet Updater made by", end=" ")
        print(Fore.LIGHTGREEN_EX + "Yondaime")
        print(Fore.RESET + "Last update was at:", end=" ")
        print(Fore.BLUE + "{}".format(datetime.now().strftime("%H:%M:%S")))
        print(Fore.RESET + "The Highscore of", end=" ")
        if highscore_found:
            print(Fore.BLUE + benchmark_names[changed_bench_index], end=" ")
        else:
            print(Fore.BLUE + "no benchmark", end=" ")
        print(Fore.RESET + "was updated")
        print(Fore.RESET + "Highscore is now", end=" ")
        if highscore_found:
            print(Fore.BLUE + str(current))
        else:
            print(Fore.BLUE + "the same")
        print(Fore.RESET + "The Average of", end=" ")
        if bench_played:
            print(Fore.BLUE + benchmark_names[changed_bench_index], end=" ")
        else:
            print(Fore.BLUE + "no benchmark", end=" ")
        print(Fore.RESET + "was updated")
        print(Fore.RESET + "Average is now", end=" ")
        if bench_played:  # If a bench was played the average could change
            print(Fore.BLUE + str(self.get_average(self, averages, changed_bench_index)))
        else:
            print(Fore.BLUE + "the same")
        print(Fore.RESET + "To stop the program press", end=" ")
        print(Fore.RED + "[Ctrl+C]")
        print(Fore.RESET + "If you have questions try reading the Readme")

