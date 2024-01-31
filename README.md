# waiverdump

A browser automation directly targeting the Resmark Waiversign website.  It is a Chrome automation using selenium webdriver.

## Installation

```bash
mkdir waiverdump
cd waiverdump
python3.12 -m venv env
source env/bin/activate
```

## Download files to the waiverdump directory

```bash
~ pip install -r requirements.txt
```

## Usage

```bash
python main.py
```
The first time the program runs the user is prompted for the userid and password to login to the Resmark website.  The credentials will be saved locally and used in subsequent runs of the program.

## Output
```
side menu is visible
 
file successfully downloaded: /home/greg/Downloads/WaiverSignParticipants-2024-01-31.csv
```
