# Progress-Sheet-Updater
This Program was made by Yondaime with much appreciated help from Nops, Knar and Pauer.

## Setup:

### Prerequisits:
You need to have a copy of the Sparky Benchmark Progress Sheet on your Google Account.  
If you do not have one already you can create a copy from here https://bit.ly/3g1HkeE  
Later on you will be asked to log in with your Google account, so if you do not fully trust this program I recommend to create the sheet on a new, empty Google Account  
Also make sure you have the statistic export in Kovaak's set to "Completion"  

#### Step One: Activating the Google Sheets API
Make sure you are using the Google Account with the Sheet for this Step!  
Go to [here](https://developers.google.com/sheets/api/quickstart/python)  
Click the "Enable Google Sheets API" Button  
Choose a Name, for example "Progress Sheet", then click Next  
Choose "Desktop app" and click "CREATE"  
Then choose "DOWNLOAD CLIENT CONFIGURATION"  
Paste the file you just downloaded into the same folder as the rest of the application  

The API you just set up will be used to dump the login credentials and to update the scores on your Spreadsheet  

#### Step Two: Setting up the Spreadsheet ID
In the same folder as the rest of the program you will find a "spreadsheetid.txt"  
Open this file and paste the ID of your spreadsheet into it  
You can find it in the Link to your Spreadsheet  
Example: http<span>s</span>://docs.google.com/spreadsheets/d/abc1234567/edit#gid=0 here the id would be "abc1234567", your ID is probably longer  
Save and exit the file  
###### Optional:  
While you are here you can also create "a path.txt" and input the path to your Kovaaks Stat folder in it  
If you choose not to you will be asked to input it later in the program  

#### Step Three: Setting up the path to the Stats folder
When you start the Program for the first time you will be asked to input the path to your Kovaaks Stats folder  
For most people the path is "C:\Program Files (x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\stats"  
Once you input the path once you will not have to input it again, unless you delete the "path.txt" that is created  

#### Step Four: Logging in into your Google Account
When you start the Program for the first time you will also be asked to grant your API Access to your Google Sheets  
Once you grant access a file called "token.pickle" will be created, this will be used to access the API from here on  


## Usage:
Once the program is running it will look through the recently exported statistics and update your Benchmark Scores if any Highscores were achieved  
In the future it will also update the average tab  
If you want to exit the program press Ctrl+C  

## Troubleshooting:
If you mistyped the path to your stats folder the program will not run, so delete the "path.txt" and start the program again  
If your "spreadsheetid.txt" is empty the program will also stop, so make sure you paste the id in  
If the Spreadsheetid in your "Spreadsheetid.txt" is wrong the program will stop, so make sure it is correct  

If you need help and the Troubleshooting is not working dm Yondaime#1370 on the [Sparky Discord](https://discord.gg/sparky)  
