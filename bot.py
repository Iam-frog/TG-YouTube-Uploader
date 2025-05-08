import os
import asyncio
import wget
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_dl import YoutubeDL
from opencc import OpenCC
from config import Config

bot = Client(
    "YT-Downloader",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN
)

YTDL_REGEX = (
    r"^((?:https?:)?\/\/)?((?:www|m)\.)?"
    r"((?:youtube\.com|youtu\.be|xvideos\.com|pornhub\.com|xhamster\.com|xnxx\.com))"
    r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$"
)
s2tw = OpenCC('s2tw.json').convert

@bot.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type == 'private':
        await message.reply(
            "<b>Hello! This is a YouTube Downloader Bot\n\nSend me a YouTube link to download audio/video.</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Channel", url="https://t.me/TeleRoidGroup"),
                 InlineKeyboardButton("Support", url="https://t.me/TeleRoid14")],
                [InlineKeyboardButton("Source Code", url="https://github.com/P-Phreak/TG-YouTube-Uploader")]
            ]),
            disable_web_page_preview=True,
            parse_mode="html"
        )

@bot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':
        await message.reply(
            "<b>YouTube Bot Help!\n\nJust send a YouTube url to download it in video or audio format.</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Channel", url="https://t.me/TeleRoidGroup"),
                 InlineKeyboardButton("Support", url="https://t.me/TeleRoid14")]
            ]),
            disable_web_page_preview=True,
            parse_mode="html"
        )

@bot.on_message(filters.private & filters.text & ~filters.edited & filters.regex(YTDL_REGEX))
async def ytdl_with_button(_, message: Message):
    await message.reply_text(
        "**Choose download type👇**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Audio 🎵", callback_data="ytdl_audio"),
             InlineKeyboardButton("Video 🎬", callback_data="ytdl_video")]
        ]),
        quote=True
    )

@bot.on_callback_query(filters.regex("^ytdl_audio$"))
async def callback_query_ytdl_audio(_, cb):
    message = cb.message
    url = message.reply_to_message.text
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': '%(title)s.%(ext)s',
        'writethumbnail': True
    }
    await cb.edit_message_text("**Downloading audio...**")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            await send_audio(message, info, file_path)
    except Exception as e:
        await message.reply_text(str(e))

@bot.on_callback_query(filters.regex("^ytdl_video$"))
async def callback_query_ytdl_video(_, cb):
    message = cb.message
    url = message.reply_to_message.text
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': '%(title)s.%(ext)s',
        'writethumbnail': True
    }
    await cb.edit_message_text("**Downloading video...**")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            await message.reply_video(video=file_path, caption=info.get("title"))
            os.remove(file_path)
    except Exception as e:
        await message.reply_text(str(e))

async def send_audio(message: Message, info, audio_file):
    basename = audio_file.rsplit(".", 1)[0]
    if info['ext'] == 'webm':
        audio_file_weba = basename + ".weba"
        os.rename(audio_file, audio_file_weba)
        audio_file = audio_file_weba

    if Config.AUDIO_THUMBNAIL.lower() != "no":
        thumb_file = wget.download(Config.AUDIO_THUMBNAIL)
    else:
        thumb_file = wget.download(info['thumbnail'])

    title = s2tw(info['title'])
    duration = int(float(info['duration']))
    performer = s2tw(info.get('uploader', ""))
    webpage_url = info.get('webpage_url', "")

    await message.reply_audio(
        audio_file,
        caption=f"<b><a href=\"{webpage_url}\">{title}</a></b>",
        duration=duration,
        performer=performer,
        title=title,
        parse_mode='HTML',
        thumb=thumb_file
    )
    os.remove(audio_file)
    os.remove(thumb_file)

if __name__ == "__main__":
    print("Bot is running...")
    bot.run()
           
