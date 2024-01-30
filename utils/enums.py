"""Module providing messages used by the bot."""


class BotMessage:
    """ class Constant for providing typical bot messages. """
    HELP = """
                -- available commands --:
<b>/start</b>   - <em>start greeting command</em>
<b>/help</b>   - <em>available commands</em>
<b>/add</b>    - <em>adding a note</em> (/add <em>actual note to remember)</em>
<b>/del</b>     - <em>deleting a note</em> (/del <em>id of note to delete)</em>
<b>/list</b>     - <em>list of all notes</em>
<b>/clear</b> - <em>delete all notes</em> [secret code:all]

<b>/ai</b>        - <em>GPT 3.5 turbo integration</em>

<b>/water</b>      - <em>sets a water reminder</em>
<b>/water_stop</b> - <em>delete the water reminder</em>
<b>/chat_description</b> - <em>change chat description</em>
<b>%delete100</b> - <em>delete from chat the last 100 messages but not older the 48 hours</em>
"""

    ADD = "...notesBot added a note..."
    DELETE = "...notesBot deleted the note: "
    NO_NOTES_BY_ID = "...there is no note with id: "
    ALL_NOTES = "...notesBot listing all notes..."
    EMPTY_LIST = "...currently no notes registered..."
    TRUNCATE = "...all notes deleted..."
    CODE = "...please provide command with the code to clear all data..."
