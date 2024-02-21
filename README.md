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
/add [note  ]    - adding a note
/del [noteId]    - delete a note
/list     - list of all notes
/clear - delete all notes [secret code:all]

/ai [question]    - GPT 3.5 turbo integration

/mp3 [youtubeLink]     - converts youtube video link to audio
/recent [channelTitle] - converts last youtube video of specified channel
/ytsearch 

/remind [topic]  - set a reminder
/stop     [topic]  - delete reminder

/chat_description - change chat description
