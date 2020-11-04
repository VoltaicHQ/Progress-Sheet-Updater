import os.path


# Create class to use functions in main.py
class Pathreader:
    # Write the path the user input into the path.txt file in the application folder
    def createpath(self, path):
        f = open("path.txt", "w")
        f.write(path)
        f.close()
        return path

    # Check if path.txt is there, if not call createpath and create it
    def getpath(self):
        pather = os.path
        if pather.exists('path.txt'):  # Check if the file exists
            f = open("path.txt", "r")  # If yes save the path in the file to scenariopath
            scenariopath = f.read()
            f.close()
            return scenariopath
        else:
            #  If it doesnt exist ask the user to input it then call createpath
            userinput = input(
                "Input the path to your Progress files, in most cases it is: \n C:\Program Files ("
                "x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\stats \n")
            assert os.path.exists(userinput), "Could not find the file, please restart the program"  # Check if path
            # exists, error if it does not
            return self.createpath(self, userinput)
