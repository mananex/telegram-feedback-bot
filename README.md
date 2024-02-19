# This is a simple telegram bot created for user feedback from moderators
### How to set up?
First, you must have a Python interpreter installed. I use Python 3.12.1, but you can use earlier versions, there should be no problems.
Before installing libraries, first create a telegram bot using [Bot Father](https://t.me/BotFather).
### Installing libraries.
I prefer using virtual environments, so let's create one and activate it!

For Windows:
```
python -m venv anonymousSupportBotVenv
cd anonymousSupportBotVenv
scripts\activate
```
For Linux:
```
python3 -m venv anonymousSupportBotVenv
cd anonymousSupportBotVenv
source bin/activate
```
Now, let's install the necessary dependencies.

For Windows:
```
pip install -r requirements.txt
```
For Linux
```
pip3 install -r requirements.txt
```
### Configuration.
Now that all the dependencies are installed, let's move on to setting up the script! Open the `configuration.py` file with any text editor. You will see this:

```
API_TOKEN         = None
DATABASE_FILENAME = 'database.db' # sqlite
LEAD_MODERATOR_ID = None
```
`API_TOKEN` is the token that BotFather gives you after creating a new bot. (value should be `str`)

`DATABASE_FILENAME` is the name of the SQLite database file. You can not change it and leave the default value.

`LEAD_MODERATOR_ID` is the telegram ID of the main moderator, who can add other moderators or remove them.
### Running the script.
Now we can finally run the script!

For Windows: `python app.py`
For Linux: `python3 app.py`

You will see these messages:
```
Creating tables...
Starting bot... Check logs.
```
and this means that the script works!
### Note.
**You can read detailed information about how the bot works in the file DETAILED.md**

