"""
The script will download the YouTube video as a mp3 file using `youtube_dl`,
and then convert it to mp3 using `pydub`.
The converted mp3 files will be saved in the 'audio_mp3' directory.
necessary packages: pip install youtube_dl pydub ffmpeg-python
"""
import logging
import os

import google_auth_oauthlib.flow
from aiogram.types import ReplyKeyboardRemove
from googleapiclient.discovery import build
import googleapiclient.errors
import youtube_dl
from aiogram import types, Router
from aiogram.filters import Command, CommandObject
from pydub import AudioSegment
from datetime import timedelta
from main import bot
from utils.util import Util
from keyboards.kb_questions import kb_download_convert

router = Router()
utilities = Util()

# Directory to store the converted mp3 files
OUTPUT_DIR = 'audio_mp3'

logger = logging.getLogger(__name__)

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


@router.message(Command("mp3"))
async def video_mp3_converter_by_youtube_link(message: types.Message, command: CommandObject):
    """"Handler to download yt video, convert it to mp3 and return audio file to client"""
    video_id = command.args.split('youtube.com/watch?v=')[1].split('&')[0]
    title = download_video(video_id)
    if title:
        await post_audio(chat_id=message.chat.id, file_url=f'{OUTPUT_DIR}/{title}.mp3', title=title)
    else:
        logger.warning("SOMETHING WENT WRONG! mp3 conversion failed...")


@router.message(Command("ConvertVideo"))
async def video_mp3_converter_by_video_id(message: types.Message, command: CommandObject):
    """"Handler for new channel posts"""
    video_id = command.args
    await message.answer(text=f"Converting video to mp3.",
                         reply_markup=ReplyKeyboardRemove())
    title = download_video(video_id)
    if title:
        await post_audio(chat_id=message.chat.id, file_url=f'{OUTPUT_DIR}/{title}.mp3', title=title)
    else:
        logger.warning("SOMETHING WENT WRONG! mp3 conversion failed...")


@router.message(Command("ytsearch"))
def ytsearch(message: types.Message, command: CommandObject):
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = ("E:\\client_secret_1070742409421-9am3v3pv2oo8cqo18aa0jsrjcp9p5pue.apps.googleusercontent.com"
                           ".json")

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    search_query = command.args
    logger.debug(search_query)
    request = youtube.search().list(
        # maxResults=10,
        # publishedAfter="2024-02-10T00:00:00Z",
        q=search_query,
        type='video',
        part='snippet',
        order='date',
    )
    response = request.execute()

    from pprint import PrettyPrinter
    pp = PrettyPrinter()
    pp.pprint(response['items'])


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
        try:
            ydl.cache.remove()
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

            # Convert the downloaded audio file to mp3 using pydub
            audio = AudioSegment.from_file(f'{OUTPUT_DIR}/{video_id}.mp3')
            title = utilities.get_page_title(f'https://www.youtube.com/watch?v={video_id}')
            audio.export(f'{OUTPUT_DIR}/{title}.mp3', format='mp3', parameters=["-ac", "2", "-ar", "8000"])

            # Remove the original audio file
            os.remove(f'{OUTPUT_DIR}/{video_id}.mp3')
            return title

        except youtube_dl.utils.DownloadError:
            logger.warning("ERROR: unable to download video data: HTTP Error 403: Forbidden")

    return None


async def post_audio(chat_id, file_url, title):
    """"Handler to post audio from local machine"""
    await bot.send_audio(chat_id,
                         types.FSInputFile(file_url, "r"),
                         performer=title,
                         title=title)


@router.message(Command("recent"))
async def get_recent_by_channel_title(message: types.Message, command: CommandObject):
    """"Handler to return recent video posts id"""
    channel_title = command.args
    api_key = os.getenv('YOUTUBE_DATA_API_KEY')

    # get client recent yesterday
    # client_datetime_now = utilities.get_client_date_time_now_from_ip_data()
    # yesterday = (client_datetime_now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=channel_title,
        part='id, snippet',
        type='video',
        order="date",
        maxResults=1,
        # publishedAfter=yesterday
    )
    result = request.execute()
    item = result['items'][0]
    await message.answer(f"{item['snippet']['description']} - {item['id']['videoId']} Choose action: ",
                         reply_markup=kb_download_convert(item['id']['videoId']))

