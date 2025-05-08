import os


class Config(object):
    TG_BOT_TOKEN = os.environ.get("7266490468:AAEQBxrhB9sZhACAKqoc2w_u6xuBkryiXWQ", "")

    APP_ID = int(os.environ.get("29639201", 12345))

    API_HASH = os.environ.get("3b1cbfcaf81a8181c6653b8d5e71f247", "")

    AUDIO_THUMBNAIL = os.environ.get("AUDIO_THUMBNAIL", "")

    VIDEO_THUMBNAIL = os.environ.get("VIDEO_THUMBNAIL", "")
