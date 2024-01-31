This is an aiogram3 bot project.

The main purpose is to familiarize with aiogram3 python library for creating telegram bots for various tasks.

For a working backend server you need:
    1. telegram account to create & access bot (creating via BotFather from telegram account)
    2. bot uses a PostgreSQL database 
    3. openAI (gpt-3.5-turbo) account

The credentials should be stored in a .env file in root directory:

    sample .env:
# telegram bot token
BOT_TOKEN = *****

# open ai token, model
OPEN_AI_API = *****
MODEL_NAME = gpt-3.5-turbo

# postgreSQL database settings
DB_HOSTNAME=*****
DB_PORT=*****
DB_NAME=*****
DB_USER=*****
DB_PASSWORD=*****

Install requirements from file requirements.txt (pip install -r requirements.txt)

                -- available bot commands --:
/start  - start greeting command
/help   - available commands
/add    - adding a note 
/del    - deleting a note 
/list   - list of all notes
/clear  - delete all notes

/ai        - GPT 3.5 turbo integration

/water      - sets a water reminder (is active between 09.00 - 20.00)
/water_stop - delete the water reminder
/chat_description - change chat description
%delete100 - delete from chat the last 100 messages but not older the 48 hours