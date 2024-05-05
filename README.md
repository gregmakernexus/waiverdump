# waiverdump

A browser automation directly targeting the Resmark Waiversign website.  It is a Chrome automation using selenium webdriver.

## Installation

This program depends on selenium so you need the chromedriver for Raspberry PI 32-bit.
```commandline
sudo apt-get install chromium-chromedriver
```

### Download package from github
```bash
git config --global credential.helper store
git clone https://github.com/gregmakernexus/waiverdump.git
```
You will be prompted for your git username and password/access token.  Once entered it will be stored.  The 'waiverdump' directory will be created.

### Create a virtual environment in the waiverdump directory and install dependencies
```bash
cd waiverdump
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# change directory to waiverdump if not already there
python main.py
```
The first time the program runs the user is prompted for the userid and password to login to the Resmark website.  The credentials will be saved locally and used in subsequent runs of the program.

## Output
```
side menu is visible
 
file successfully downloaded: /home/greg/Downloads/WaiverSignParticipants-2024-01-31.csv
```
