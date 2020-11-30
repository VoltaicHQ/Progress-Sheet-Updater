from colorama import Fore
from datetime import datetime
import os

# This class handles console output
class consoleOutput:

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Create console output, varies depending on if a benchmark was played and if a highscore was found
    def create_output(self, scens):
        hs_found = False
        avg_found = False
        #self.cls(self)
        print("Progress Sheet Updater made by", end=" ")
        print(Fore.LIGHTGREEN_EX + "Yondaime & Knar")
        print(Fore.RESET + "Last update was at:", end=" ")
        print(Fore.BLUE + "{}".format(datetime.now().strftime("%H:%M:%S")))
        print(Fore.RESET + "The Highscore of", end=" ")
        for s in scens:
            if scens[s]['hs_updated']:
                print(Fore.BLUE + str(s), end=" ")
                print(Fore.RESET + "got updated")
                print("Highscore is now", end=" ")
                print(Fore.BLUE + str(scens[s]['hs']))
                hs_found = True
        if not hs_found:
            print(Fore.BLUE + "no benchmark", end=" ")
            print(Fore.RESET + "got updated")
        print(Fore.RESET + "The Average of", end=" ")
        for s in scens:
            if scens[s]['avg_updated']:
                print(Fore.BLUE + str(s), end=" ")
                print(Fore.RESET + "was updated")
                print(Fore.RESET + "Average is now", end=" ")
                print(Fore.BLUE + str(scens[s]['avg']))
                avg_found = True
        if not avg_found:
            print(Fore.BLUE + "no benchmark", end=" ")
            print(Fore.RESET + "was updated")
            print(Fore.RESET + "Average is still", end=" ")
            print(Fore.BLUE + "the same")
        print(Fore.RESET + "If you have questions try reading the Readme")
