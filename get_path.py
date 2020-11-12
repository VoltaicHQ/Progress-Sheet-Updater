import os.path
import sys

# This class handles the methods needed to process the path into path.txt
class pathReader:
    # Write the path the user input into the path.txt file in the application folder
    def create_path(self, path):
        f = open("path.txt", "w")
        f.write(path)
        f.close()
        return path

    # Check if path.txt is there, if not call createpath and create it
    def get_path(self):
        pather = os.path
        if pather.exists('path.txt'):  # Check if the file exists
            f = open("path.txt", "r")  # If yes read the path in the file
            scenariopath = f.read()
            f.close()
            return scenariopath
        else:
            #  If it doesnt exist ask the user to input it then call createpath
            user_input = input(
                "Input the path to your Progress files, in most cases it is: \n C:\Program Files ("
                "x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\stats \n")
            try:
                assert os.path.exists(user_input)
            # Check if path exists, error if it does not
            except AssertionError:
                f = open("error.txt", "w")
                f.write(
                    "Could not find the path you specified, make sure you input the correct one")
                f.close()
                sys.exit()
            return self.create_path(self, user_input)
