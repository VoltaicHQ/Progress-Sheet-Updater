# Progress-Sheet-Updater
This Program was made by the Voltaic Dev Team

## Setup:

### Prerequisits:
You need a Google Account, so if you do not own one already create one now.
You need to have a copy of the Voltaic Benchmark Progress Sheet on your Google Account.  
If you do not have one already you can create a copy from [here](https://docs.google.com/spreadsheets/d/1oloiojSWGmgdId5f248HH-uteIONwEgm4FCYUlmp5FU/edit#gid=1324419980).  
Also make sure you have the statistic export setting in Kovaak's set to "Challenge Completion".  
![Statisticexport](/readmeimages/statisticexport.png)  

### Step One: Downloading the Program
Go to the [Release](https://github.com/Y0ndaime/Progress-Sheet-Updater/releases) part of this repository and download the newest .zip.  
![Release](/readmeimages/release.png)  
Once downloaded extract the folder inside the .zip to the place where you want to have it.  
This folder is where you will have to put the files in the next steps.

### Step Two: Activating the Google Sheets API
Make sure you are using the Google Account with the Sheet for this Step!  
Go to [here](https://developers.google.com/sheets/api/quickstart/python).  
Click the "Enable Google Sheets API" Button.  
![Enable Sheets API](/readmeimages/enablegooglesheetsapi.png)  
Choose a Name, for example "Progress Sheet", then click Next.  
![API name](/readmeimages/apiname.png)  
Choose "Desktop app" and click "CREATE".  
![Desktopapp](/readmeimages/desktopapp.png)  
Then choose "DOWNLOAD CLIENT CONFIGURATION".  
![Downloadclientconfig](/readmeimages/downloadclientconfig.png)  
Paste the file you just downloaded (credentials.json) into the same folder as the rest of the application.  

The API you just set up will be used to dump the login credentials and to update the scores on your Spreadsheet.  

### Step Three: Setting up the config.json
In the same folder as the rest of the program you will find a "config.json".  
Open this file in the editor of your choice, it should look like this:  
![config](/readmeimages/config.png)  
You can edit the options in this config to your liking.  
#### "path_to_stats":  
Here you input the path to your Kovaak's stats folder, for most people it is  
"C:\Program Files (x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\stats".    
#### "link_to_sheet":  
Here you input the link to your Progression Sheet.  
#### "highscore_ranges":  
Here you input the range where the highscores will be pasted into, keep them at the preset if you do not wish to add extra scenarios to track.  
#### "average_ranges":  
Here you input the range where the averages will be pasted into, keep them at the preset if you do not wish to add extra scenarios to track.  
#### "update_sheet_on_startup":  
If "true" this updates your sheet on startup of the program, using all runs u played even when the program was not running.  
If "false" this will not update your sheet on startup.  
#### "calculate_averages":  
If "true" the program calculates the averages of your last x runs.  
If "false" it does not.  
#### "num_of_runs_to_average":  
Here you input the number of runs you want to use to calculate the averages.  
#### "polling_interval":  
Here you input the time between updates to the sheet.  
Polling rates lower than 60 are not advised to use.

In the end it should look similar to this.  
![configexample](/readmeimages/configexample.png)  
Save and exit the file.  

### Step Four: Logging in into your Google Account
When you start the Program for the first time you will also be asked to grant your API Access to your Google Sheets.  
Once you grant access a file called "token.pickle" will be created, this will be used to access the API from here on.  

## Usage:

After setting everything up correctly you can let the program run in the background while you play Kovaak's.  
It will detect if you played a Voltaic Benchmark and automatically update your Progress Sheet.  
If you want you can open the console window on a second monitor and it will give you feedback on what has changed.  
You can also just open your Progress Sheet and it will update in real time.
You can also use it to update your Progress Sheet manually, by setting "update_sheet_on_startup" to "true" and running the program for a short time.


## Troubleshooting:

If your program crashes, you can take a look at the error message in the console window.  
If you did not read it there it should also exist in a file called "error.txt".  

If you need help and the Troubleshooting is not working dm Yondaime#1370 on the [Voltaic Discord](https://discord.gg/voltaic)  
