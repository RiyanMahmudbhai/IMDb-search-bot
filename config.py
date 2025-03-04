from pyrogram import filters

class Config:
    BOT_TOKEN = "7855160486:AAGW8E-BtC2gSxv_PiWoj1PrJHwwp9fcyUQ"
    API_ID = "25902474"
    API_HASH = "e0613c7a7b94e0025a20f5cf7bc69eee"
    IMDB_TEMPLATE = """
🏷 <b>Title</b>: <b>{title}</b> [{year}]
🎭 <b>Genres</b>: {genres}
🌟 <b>Rating</b>: {rating} (based on {votes} user ratings)
☀️ <b>Languages</b>: {languages}
📀 <b>Runtime</b>: {runtime}
📆 <b>Release Info</b>: {release_date}
🎛 <b>Countries</b>: {countries}

📖 <b>Storyline</b>:
<i>{plot}</i>
    """
    # Add other configurations as needed

config_dict = Config()
