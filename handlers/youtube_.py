"""
The script will download the YouTube video as a mp3 file using `youtube_dl`,
and then convert it to mp3 using `pydub`.
The converted mp3 files will be saved in the 'mp3_files' directory.
necessary packages: pip install youtube_dl pydub ffmpeg-python
"""
import logging
import os
import youtube_dl
from aiogram import types, Router
from aiogram.filters import Command, CommandObject
from pydub import AudioSegment

from main import bot
from utils.util import Util

router = Router()
util = Util()

# YouTube channel URL you want to follow
CHANNEL_URL = 'https://www.youtube.com/@plushev'

# Directory to store the converted mp3 files
OUTPUT_DIR = 'audio_mp3'

logger = logging.getLogger(__name__)

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


@router.chat_member()
async def handle_new_chat_member(message: types.Message):
    """" Handler for new messages"""
    await message.reply('Thanks for adding me to the group!')


@router.message(Command("mp3"))
async def handle_new_channel_post(message: types.Message, command: CommandObject):
    """"Handler for new channel posts"""
    # # Check if the channel post is from the specified channel
    # if message.chat.username == CHANNEL_URL.split('/')[-1]:
    #     # Extract the YouTube video ID from the message text
    #     video_id = message.text.split('youtube.com/watch?v=')[1].split('&')[0]
    #
    #     # Download the YouTube video as mp3
    #     download_video(video_id)

    video_id = command.args.split('youtube.com/watch?v=')[1].split('&')[0]
    title = download_video(video_id)
    await post_audio(chat_id=message.chat.id, file_url=f'{OUTPUT_DIR}/{title}.mp3', title=title)


def download_video(video_id):
    """" Function to download a YouTube video as mp3"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{OUTPUT_DIR}/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '190',
        }],
        # 'postprocessor_args': [
        #     '-compression_level', '8',  # Sets the compression level to maximum
        #     '-aq', '1',  # Sets the audio quality to 0 (minimum)
        #     '-ac', '2'  # Sets the number of audio channels to 2 (stereo)
        # ],
        # 'ffmpeg_location': '/usr/local/bin/ffmpeg',  # Path to ffmpeg binary
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

    # Convert the downloaded audio file to mp3 using pydub
    audio = AudioSegment.from_file(f'{OUTPUT_DIR}/{video_id}.mp3')
    title = util.get_page_title(f'https://www.youtube.com/watch?v={video_id}')
    audio.export(f'{OUTPUT_DIR}/{title}.mp3', format='mp3', parameters=["-ac", "2", "-ar", "8000"])

    # Remove the original audio file
    os.remove(f'{OUTPUT_DIR}/{video_id}.mp3')
    return title


async def post_audio(chat_id, file_url, title):
    await bot.send_audio(chat_id,
                         types.FSInputFile(file_url, "r"),
                         performer=title,
                         title=title)


@router.message(Command("data"))
async def handle_get_data(message: types.Message, command: CommandObject):
    """"Handler for new channel posts"""
    url = command.args
    util.get_data(url)
