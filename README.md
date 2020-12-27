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

3. Open `config.json` with Notepad (right-click it -> Open with -> Notepad) or your text editor of choice. Copy your sheet's ID from the URL of your progress sheet. The ID is highlighted in the sample image below. 

![Sheet ID from URL](/readmeimages/sheet_id_from_url.png) 

Replace the placeholder `sheed_id` text with your sheet's ID. Save and close the file.

```
{
    ...
    "sheet_id": "175i2Us2Vyi3eauSe5rWE94KE4DmIJE_iusa2d4OvC3E",
    ...
}
```
If your steam library is not installed in the default folder location then you will need to edit the `stats_path` as well.

5. Run `ProgressSheetUpdater.exe`. The first time you do so you will be prompted to:

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
