from pyrogram import filters

class Config:
    BOT_TOKEN = "YOUR_BOT_TOKEN"
    API_ID = "YOUR_API_ID"
    API_HASH = "YOUR_API_HASH"
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
