<h1 align="center">Progress Sheet Updater</h1>
<p align="center">
    <img width="300" alt="Screenshot" src="readmeimages/screenshot.gif">
</p>

## About

This tool updates your [Voltaic Benchmark Progress Sheet](https://docs.google.com/spreadsheets/d/1L6iCXTaSheZtVwtVR4b_FYJzcCZbEYVRsdFo7PI3HTk/) with high scores and averages of completed challenges on [KovaaK](https://store.steampowered.com/app/824270/KovaaK_20/).

Run it before checking your progress sheet, or leave it running in the background to keep your sheet up-to-date as you play.

Easily keep track of additional scenarios beyond the scope of the Voltaic Benchmarks through the configuration file.

## Quickstart Guide
1. Make a copy of the [Voltaic Benchmark Progress Sheet](https://docs.google.com/spreadsheets/d/1L6iCXTaSheZtVwtVR4b_FYJzcCZbEYVRsdFo7PI3HTk/) if you don't already have one. This requires a Google account.

2. Download and extract the latest release of this tool from [here](https://github.com/VoltaicHQ/Progress-Sheet-Updater/releases). I recommend [7zip](https://www.7-zip.org/) for extracting zip files.

2. Go [here](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the), and ensure you are logged in to the same Google Account that owns your progress sheet. Then:

    1. Click the blue `Enable Google Sheets API` button.
    2. Click `Next` in the bottom-right.
    3. Click `Create` in the bottom-right.
    4. Click the blue `DOWNLOAD CLIENT CONFIGURATION` button.
    5. Move the downloaded `credentials.json` file into the extracted folder, alongside `ProgressSheetUpdater.exe` and `config.json`. Like so:
    
<p align="center">
    <img alt="Folder contents before oauth" src="readmeimages/folder_contents_before_auth.png">
</p>

3. Run `ProgressSheetUpdater.exe`. A GUI will open, this GUI is used to edit the configuration of the program.
    
    1. Click the `Browse`-Button on the top left and navigate to your Kovaak's stats folder.
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

    4. The first time you run the program you will be prompted to:

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
