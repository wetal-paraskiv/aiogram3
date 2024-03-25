"""Module providing messages used by the bot."""


class BotMessage:
    """ class Constant for providing typical bot messages. """
    HELP = """
                -- available commands --:
<b>/start</b>  - <em>greeting command</em>
<b>/help</b>   - <em>available commands</em>
<b>/add [note  ]</b>    - <em>adding a note</em>
<b>/del [noteId]</b>    - <em>delete a note</em>
<b>/list</b>     - <em>list of all notes</em>
<b>/clear</b> - <em>delete all notes</em> [secret code:all]

<b>/ai [question]</b>    - <em>GPT 3.5 turbo integration</em>
<b>/dict [word]</b>    - <em>word meaning by GPT 3.5 turbo</em>

<b>/mp3 [youtubeLink]</b>     - <em>converts youtube video link to audio</em>
<b>/recent [channelTitle]</b> - <em>returns last youtube video id</em>
<b>/ytsearch [channelTitle]</b> - <em>returns list of youtube videos id</em>

<b>/remind [topic]</b>  - <em>set a reminder</em>
<b>/stop     [topic]</b>  - <em>delete reminder</em>

<b>/chat_description</b> - <em>change chat description</em>
"""

    ADD = "...notesBot added a note..."
    NONE_NOTE = "...there wasn't any note text..."
    DELETE = "...notesBot deleted the note: "
    NO_NOTES_BY_ID = "...there is no note with id: "
    ALL_NOTES = "...notesBot listing all notes..."
    EMPTY_LIST = "...currently no notes registered..."
    TRUNCATE = "...all notes deleted..."
    CODE = "...please provide command with the code to clear all data..."
