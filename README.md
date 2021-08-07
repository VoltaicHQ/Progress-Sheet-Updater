<h1 align="center">Progress Sheet Updater</h1>
<p align="center">
    <img width="300" alt="Screenshot" src="readmeimages/screenshot.gif">
</p>

## About

This tool updates your [Voltaic Benchmark Progress Sheet](https://docs.google.com/spreadsheets/d/1L6iCXTaSheZtVwtVR4b_FYJzcCZbEYVRsdFo7PI3HTk/) with high scores and averages of completed challenges on [KovaaK](https://store.steampowered.com/app/824270/KovaaK_20/).

Run it before checking your progress sheet, or leave it running in the background to keep your sheet up-to-date as you play.

If you use multiple configs you can just drag them into the .exe to make your life easier

Easily keep track of additional scenarios beyond the scope of the Voltaic Benchmarks through the configuration file.

## Updating

If you want to update to a newer release all you have to do is download the newest one. Then move the ProgressSheetUpdater.exe over into your old folder.  

## Quickstart Guide

####    This Guide is also available as a [video](https://www.youtube.com/watch?v=awBoG9Jy8CY) (please make sure to check the pinned comment of the video for further information)

1. Make a copy of the [Voltaic Benchmark Progress Sheet](https://docs.google.com/spreadsheets/d/1yHj87rQNW2WsuH24UoKZajNwNpI6CVyUjR3AwBMbnnY/edit#gid=1324419980/) if you don't already have one. This requires a Google account.

2. Download and extract the latest release of this tool from [here](https://github.com/VoltaicHQ/Progress-Sheet-Updater/releases). I recommend [7zip](https://www.7-zip.org/) for extracting zip files.

3. Go [here](https://developers.google.com/workspace/guides/create-project), and ensure you are logged in to the same Google Account that owns your progress sheet. Then:  
    (Since Google has updated their site this now takes more work than before.)  

    1. Click the link in step 1 of the `Create a new Google Cloud Platform (GCP) project, Google Cloud Console`  
    2. At the top left, next to `Google Cloud Platform`, click `Select a project`
    3. Click `NEW PROJECT` at the top right corner of the new window that pops up
    4. Type any name you like in the `Project Name` field and click the `CREATE` button under the `Location` field
    5. Wait until a green check mark shows up in the notification window at the top right of the window indicating that the creation of your project is complete. Then click APIs & Services on the menu to the left
    6. Click the project you just created
    7. The Google Sheets API might show up in the list at the bottom - click it if it does. If not, click the `ENABLE APIS AND SERVICES` button at the top. Click the `Search for APIs & Services` text field and type `Google Sheets API`. Click the `Google Sheets API` box. Click `Enable` and wait for it to open
    8. Click `Credentials` on the menu to the left
    9. Click the `Create Credentials` button near the top and select `OAuth client ID`
    10. Click the `CONFIGURE CONSENT SCREEN` button on the right
    11. Select the `External` option and click the `CREATE` button underneath it
    12. In the `App information` section—in the `App name` field, type whatever you want to name your app. In the `User support email` field, type the email address for the Google account that owns your progress sheet. In the `Developer contact information` section near the bottom of the page—in the `Email addresses` field, type the email address for the Google account that owns your progress sheet
    13. Click the `SAVE AND CONTINUE` button at the bottom of the page
    14. Click the `ADD OR REMOVE SCOPES` button
    15. In the `Update selected scopes` menu that opens on the right side of the screen, at the bottom, under the `Manually add scopes` section, paste ht<span>tps://ww</span>w.googleapis.com/auth/spreadsheets in the text box and click the `ADD TO TABLE` button underneath
    16. Click the `UPDATE` button at the bottom of the menu, then click the `SAVE AND CONTINUE` button at the bottom
    17. Click the `ADD USERS` button, type the email address for the Google account that owns your progress sheet into the text box on the right and click the `ADD` button underneath it
    18. Click the `SAVE AND CONTINUE` button
    19. Click `Credentials` on the left menu
    20. Click the `CREATE CREDENTIALS` button at the top and select `OAuth client ID`
    21. Click the `Application type` drop-down menu and select `Desktop application`
    22. In the `Name` field, write whatever name you want and click the `Create` button at the bottom.
    23. Click the `OK` button
    24. Under the `OAuth 2.0 Client IDs` section, your ID will be listed. Click the download icon on the far right of the row of your newly created ID
    25. Name it `credentials.json` and save it in the folder with the rest of the program
    
<p align="center">
    <img alt="Folder contents before oauth" src="readmeimages/folder_contents_before_auth.png">
</p>

4. Run `ProgressSheetUpdater.exe`. A GUI will open, this GUI is used to edit the configuration of the program.
    
    1. Click the `Browse`-Button on the top right and navigate to your Kovaak's stats folder.  
    2. Paste the link to your Progress Sheet into the entryfield.  
    3. Check the settings that you wish to use.  
        `Calculate Averages`: The Program will calculate and fill the average columns  
        `Open Config`: The GUI window will open when the program is started (if you disable this you have to manually reenable it by editing the `config.json`)  
        `Polling Interval`: Time between updates when using the `interval` Run Mode  
        `Number of runs to average`: Amount of runs used to calculate the averages  
        `Run Mode`: Types of updating the scores  
         1. `once`: Program will run once and then close  
         2. `watchdog`: Program will update sheet once a new score is added  
         3. `interval`: Program will update sheet once every x seconds  
        `Add/Remove Range`: Used to add/remove scenarios to track, it is recommended to not change this setting unless you know what you are doing  

5. The first time you run the program you will be prompted to:

        1. Choose the account that owns your progress sheet.
        2. Click `Advanced` in the bottom-left, then `Go to Quickstart (unsafe)`.
        3. Click `Allow`.
        4. Click `Allow` again. A file called `token.pickle` will be saved to avoid future prompts.
        
## Build It Yourself

Windows with Python 3.7+,

```bash
$ git clone https://github.com/VoltaicHQ/Progress-Sheet-Updater
$ cd Progress-Sheet-Updater
$ pip install -r requirements.txt
```

Edit the paths in `main.spec` to match your setup.

```bash
$ pyinstaller main.spec main.py
```
