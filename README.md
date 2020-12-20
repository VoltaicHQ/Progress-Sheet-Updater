<h1 align="center">Progress Sheet Updater</h1>
<p align="center">
    <img width="200" alt="Screenshot" src="readmeimages/screenshot.png">
</p>

## About

This tool updates your [Voltaic Benchmark Progress Sheet](https://docs.google.com/spreadsheets/d/1oloiojSWGmgdId5f248HH-uteIONwEgm4FCYUlmp5FU/) with high scores and averages of completed challenges on [KovaaK](https://store.steampowered.com/app/824270/KovaaK_20/).

Run it before checking your progress sheet, or leave it running in the background to keep your sheet up-to-date as you play.

Easily keep track of additional scenarios beyond the scope of the Voltaic Benchmarks through the configuration file.

## Quickstart Guide

1. [Download]() and extract the latest release.

2. Go [here](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the), and ensure you are logged in to the same Google Account that owns your progress sheet.

    1. Click the blue `Enable Google Sheets API` button.
    2. Click `Next` in the bottom-right.
    3. Click `Create` in the bottom-right.
    4. Click the blue `DOWNLOAD CLIENT CONFIGURATION` button.
    5. Move the `credentials.json` file to your extracted folder, alongside `ProgressSheetUpdater.exe` and `config.json`.
    
    ![Folder contents before oauth](/readmeimages/folder_contents_before_auth.png)

3. Open `config.json` your text editor of choice and add your sheet's ID. Then save and close the file.

![Sheet ID from URL](/readmeimages/sheet_id_from_url.png) 

```
{
    ...
    "sheet_id": "175i2Us2Vyi3eauSe5rWE94KE4DmIJE_iusa2d4OvC3E",
    ...
}
```

4. Run `ProgressSheetUpdater.exe`.

    1. Choose the account that owns your progress sheet.
    2. Click `Advanced` in the bottom-left, then `Go to Quickstart (unsafe)`.
    3. Click `Allow`.
    4. Click `Allow` again. A file called `token.pickle` will be saved to avoid future prompts.

5. Beat your high scores.

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