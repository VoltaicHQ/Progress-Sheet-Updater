<h1 align="center">Progress Sheet Updater</h1>
<p align="center">
    <img width="300" alt="Screenshot" src="readmeimages/screenshot.gif">
</p>

## About

This tool updates your [Voltaic Benchmark Progress Sheet](https://docs.google.com/spreadsheets/d/1L6iCXTaSheZtVwtVR4b_FYJzcCZbEYVRsdFo7PI3HTk/) with high scores and averages of completed challenges on [KovaaK](https://store.steampowered.com/app/824270/KovaaK_20/).

Run it before checking your progress sheet, or leave it running in the background to keep your sheet up-to-date as you play.

Easily keep track of additional scenarios beyond the scope of the Voltaic Benchmarks through the configuration file.

## Quickstart Guide

####    This Guide is also available as a [video](https://youtu.be/BDUUy-ajyrk) (note that the video is missing the third part of this written guide due to google updates, so you will have to follow this written guide for it)

1. Make a copy of the [Voltaic Benchmark Progress Sheet](https://docs.google.com/spreadsheets/d/1L6iCXTaSheZtVwtVR4b_FYJzcCZbEYVRsdFo7PI3HTk/) if you don't already have one. This requires a Google account.

2. Download and extract the latest release of this tool from [here](https://github.com/VoltaicHQ/Progress-Sheet-Updater/releases). I recommend [7zip](https://www.7-zip.org/) for extracting zip files.

3. Go [here](https://developers.google.com/workspace/guides/create-project), and ensure you are logged in to the same Google Account that owns your progress sheet. Then:  
    (Since Google has updated their site this now takes more work than before.)  

    1. Follow the steps of the upper guide, you dont need to enable the `Google Sheets API` since it is enabled by default
    2. Click the `menu button` on the top left
    3. Choose `APIs & Services`
    5. Type `Google Sheets API` from the list of APIs in the bottom, and add it to your project if it isn't already
    6. Click the `menu button` on the top left
    7. Choose `APIs & Services`
    8. Choose the `Google Sheets API` from the list in the bottom
    9. Click `Credentials`
    10. Click the `Create Credentials` button on the middle right
    11. Choose the `Google Sheets API`
    12. Choose `Other UI`
    13. Choose `User data`
    14. Click `What credentials do I need?`
    15. Click `SET UP CONSENT SCREEN`
    16. Choose `external`
    17. Enter the information (don't worry only you will be able to see whatever you enter)
    18. Click `ADD OR REMOVE SCOPES`, then paste `https://www.googleapis.com/auth/spreadsheets` into the textfield on the bottom and click `ADD TO TABLE`
    19. Click `UPDATE`, then click `SAVE AND CONTINUE`
    20. Click `ADD USERS` and add your email address into the Test users and save the changes
    21. Choose `Credentials` in the bar on the right
    22. Press `CREATE CREDENTIALS`, choose `OAuth client ID`
    23. Choose `Desktop app`, give it a name and click `CREATE`
    24. Click the download button on the right in the row of the ID you just created. Rename the file to `credentials.json`
    25. Place `credentials.json` into the folder with the rest of the program
    
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
        
## Updating to v1.1
 If you already used version 1.0 and now want to update, you can download the new release, and move over the `token.pickle`  
 and the `credentials.json` from your old folder to the new one. Make sure that you use the new `config.json`.

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
