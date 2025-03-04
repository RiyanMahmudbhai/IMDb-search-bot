from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler  # Add this import
from pyrogram.errors import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from pyrogram import idle
from imdb import Cinemagoer
from pycountry import countries as conn
import re
from contextlib import suppress
from datetime import timedelta
from config import config_dict
import logging
logging.basicConfig(level=logging.INFO)


# Initialize client
bot = Client(
    "imdb_bot",
    api_id=config_dict.API_ID,
    api_hash=config_dict.API_HASH,
    bot_token=config_dict.BOT_TOKEN
)


imdb = Cinemagoer()

IMDB_GENRE_EMOJI = {"Action": "🚀", "Adult": "🔞", "Adventure": "🌋", "Animation": "🎠", "Biography": "📜", "Comedy": "🪗", "Crime": "🔪", "Documentary": "🎞", "Drama": "🎭", "Family": "👨‍👩‍👧‍👦", "Fantasy": "🫧", "Film Noir": "🎯", "Game Show": "🎮", "History": "🏛", "Horror": "🧟", "Musical": "🎻", "Music": "🎸", "Mystery": "🧳", "News": "📰", "Reality-TV": "🖥", "Romance": "🥰", "Sci-Fi": "🌠", "Short": "📝", "Sport": "⛳", "Talk-Show": "👨‍🍳", "Thriller": "🗡", "War": "⚔", "Western": "🪩"}
LIST_ITEMS = 4

class ButtonMaker:
    def __init__(self):
        self.button = []
        self.header_button = []
        self.footer_button = []

    def ibutton(self, key, data, position=None):
        if not position:
            self.button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'header':
            self.header_button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'footer':
            self.footer_button.append(InlineKeyboardButton(text=key, callback_data=data))

    def build_menu(self, n_cols):
        menu = [self.button[i:i + n_cols] for i in range(0, len(self.button), n_cols)]
        if self.header_button:
            menu.insert(0, self.header_button)
        if self.footer_button:
            menu.append(self.footer_button)
        return InlineKeyboardMarkup(menu)


# Add these functions to your code
def get_readable_time(seconds: int) -> str:
    periods = [('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name} '
    return result.strip()

async def sendMessage(message: Message, text, buttons=None, photo=None):
    if photo:
        return await message.reply_photo(photo=photo, caption=text, reply_markup=buttons)
    return await message.reply(text, reply_markup=buttons)

async def editMessage(message: Message, text, buttons=None):
    await message.edit(text, reply_markup=buttons)



async def imdb_search(_, message):
    if ' ' in message.text:
        k = await sendMessage(message, '<code>Searching IMDB ...</code>')
        title = message.text.split(' ', 1)[1]
        user_id = message.from_user.id
        buttons = ButtonMaker()
        if title.lower().startswith("https://www.imdb.com/title/tt"):
            movieid = title.replace("https://www.imdb.com/title/tt", "")
            if movie := imdb.get_movie(movieid):
                buttons.ibutton(f"🎬 {movie.get('title')} ({movie.get('year')})", f"imdb {user_id} movie {movieid}")
            else:
                return await editMessage(k, "<i>No Results Found</i>")
        else:
            movies = get_poster(title, bulk=True)
            if not movies:
                return editMessage("<i>No Results Found</i>, Try Again or Use <b>Title ID</b>", k)
            for movie in movies: # Refurbished Soon !!
                buttons.ibutton(f"🎬 {movie.get('title')} ({movie.get('year')})", f"imdb {user_id} movie {movie.movieID}")
        buttons.ibutton("🚫 Close 🚫", f"imdb {user_id} close")
        await editMessage(k, '<b><i>Here What I found on IMDb.com</i></b>', buttons.build_menu(1))
    else:
        await sendMessage(message, '<i>Send Movie / TV Series Name along with /imdb Command or send IMDB URL</i>')


def get_poster(query, bulk=False, id=False, file=None):
    if not id:
        query = (query.strip()).lower()
        title = query
        year = re.findall(r'[1-2]\d{3}$', query, re.IGNORECASE)  # Fixed
        if year:
            year = list_to_str(year[:1])
            title = (query.replace(year, "")).strip()
        elif file is not None:
            year = re.findall(r'[1-2]\d{3}', file, re.IGNORECASE)  # Fixed
            if year:
                year = list_to_str(year[:1])
        # ... rest of the function ...
        else:
            year = None
        movieid = imdb.search_movie(title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered = list(filter(lambda k: str(k.get('year')) == str(year), movieid)) or movieid
        else:
            filtered = movieid
        movieid = list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered)) or filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = query
    movie = imdb.get_movie(movieid)
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    plot = movie.get('plot')
    plot = plot[0] if plot and len(plot) > 0 else movie.get('plot outline')
    if plot and len(plot) > 300:
        plot = f"{plot[:300]}..."
    return {
        'title': movie.get('title'),
        'trailer': movie.get('videos'),
        'votes': movie.get('votes'),
        "aka": list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        "box_office": movie.get('box office'),
        'localized_title': movie.get('localized title'),
        'kind': movie.get("kind"),
        "imdb_id": f"tt{movie.get('imdbID')}",
        "cast": list_to_str(movie.get("cast")),
        "runtime": list_to_str([get_readable_time(int(run) * 60) for run in movie.get("runtimes", "0")]),
        "countries": list_to_hash(movie.get("countries"), True),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_hash(movie.get("languages")),
        "director": list_to_str(movie.get("director")),
        "writer":list_to_str(movie.get("writer")),
        "producer":list_to_str(movie.get("producer")),
        "composer":list_to_str(movie.get("composer")) ,
        "cinematographer":list_to_str(movie.get("cinematographer")),
        "music_team": list_to_str(movie.get("music department")),
        "distributors": list_to_str(movie.get("distributors")),
        'release_date': date,
        'year': movie.get('year'),
        'genres': list_to_hash(movie.get("genres"), emoji=True),
        'poster': movie.get('full-size cover url'),
        'plot': plot,
        'rating': str(movie.get("rating"))+" / 10",
        'url':f'https://www.imdb.com/title/tt{movieid}',
        'url_cast':f'https://www.imdb.com/title/tt{movieid}/fullcredits#cast',
        'url_releaseinfo':f'https://www.imdb.com/title/tt{movieid}/releaseinfo',
    }

def list_to_str(k):
    if not k:
        return ""
    elif len(k) == 1:
        return str(k[0])
    elif LIST_ITEMS:
        k = k[:int(LIST_ITEMS)]
        return ' '.join(f'{elem},' for elem in k)[:-1]+' ...'
    else:
        return ' '.join(f'{elem},' for elem in k)[:-1]

def list_to_hash(k, flagg=False, emoji=False):
    listing = ""
    if not k:
        return ""
    elif len(k) == 1:
        if not flagg:
            if emoji:
                return str(IMDB_GENRE_EMOJI.get(k[0], '')+" #"+k[0].replace(" ", "_").replace("-", "_"))
            return str("#"+k[0].replace(" ", "_").replace("-", "_"))
        try:
            conflag = (conn.get(name=k[0])).flag
            return str(f"{conflag} #" + k[0].replace(" ", "_").replace("-", "_"))
        except AttributeError:
            return str("#"+k[0].replace(" ", "_").replace("-", "_"))
    elif LIST_ITEMS:
        k = k[:int(LIST_ITEMS)]
        for elem in k:
            ele = elem.replace(" ", "_").replace("-", "_")
            if flagg:
                with suppress(AttributeError):
                    conflag = (conn.get(name=elem)).flag
                    listing += f'{conflag} '
            if emoji:
                listing += f"{IMDB_GENRE_EMOJI.get(elem, '')} "
            listing += f'#{ele}, '
        return f'{listing[:-2]}'
    else:
        for elem in k:
            ele = elem.replace(" ", "_").replace("-", "_")
            if flagg:
                conflag = (conn.get(name=elem)).flag
                listing += f'{conflag} '
            listing += f'#{ele}, '
        return listing[:-2]

async def imdb_callback(_, query):
    try:
        message = query.message
        user_id = query.from_user.id
        data = query.data.split()
        
        if user_id != int(data[1]):
            await query.answer("Not Yours!", show_alert=True)
            return
            
        if data[2] != "movie":
            await query.answer()
            await query.message.delete()
            return

        await query.answer()
        imdb_data = get_poster(query=data[3], id=True)
        buttons = []
        
        # Handle trailer button
        if imdb_data.get('trailer'):
            trailer_url = imdb_data['trailer'][-1] if isinstance(imdb_data['trailer'], list) else imdb_data['trailer']
            buttons.append([InlineKeyboardButton("▶️ IMDb Trailer", url=trailer_url)])
        
        # Add close button
        buttons.append([InlineKeyboardButton("🚫 Close", callback_data=f"imdb {user_id} close")])
        
        # Safe chat ID and reply ID handling
        if message.reply_to_message:
            chat_id = message.reply_to_message.chat.id
            reply_id = message.reply_to_message.id
            target_message = message.reply_to_message
        else:
            chat_id = message.chat.id
            reply_id = message.id
            target_message = message

        # Generate caption from template
        template = config_dict.IMDB_TEMPLATE
        if not imdb_data or not template:
            await query.answer("No results found!", show_alert=True)
            return
            
        caption = template.format(
            title=imdb_data.get('title', 'N/A'),
            year=imdb_data.get('year', 'N/A'),
            # Add all other format fields here...
            plot=imdb_data.get('plot', 'No plot available')
        )

        # Try sending poster photo
        try:
            if imdb_data.get('poster'):
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=imdb_data['poster'],
                    caption=caption,
                    reply_to_message_id=reply_id,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            else:
                await sendMessage(
                    target_message,
                    caption,
                    InlineKeyboardMarkup(buttons),
                    'https://telegra.ph/file/5af8d90a479b0d11df298.jpg'
                )
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            # Fallback to different poster size
            if imdb_data.get('poster'):
                fallback_poster = imdb_data['poster'].replace('.jpg', "._V1_UX360.jpg")
                await sendMessage(target_message, caption, InlineKeyboardMarkup(buttons), fallback_poster)

        # Cleanup
        with suppress(Exception):
            await message.delete()
            if message.reply_to_message:
                await message.reply_to_message.delete()

    except Exception as e:
        print(f"Error in callback handler: {e}")
        await query.answer("An error occurred, please try again!", show_alert=True)


# Register handlers
bot.add_handler(MessageHandler(imdb_search, filters.command("imdb")))
bot.add_handler(CallbackQueryHandler(imdb_callback, filters.regex(r'^imdb')))


@bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("🎬 IMDb Search Bot Ready!\nUse /imdb <movie/tv name> to search")

# Previous code remains the same until...

app = Client("my_account")

async def main():
    await bot.start()
    print("Bot started successfully! Send /start to test")
    await idle()  # Call idle directly, not bot.idle()
    await bot.stop()

if __name__ == "__main__":
    print("Starting bot...")
    bot.run(main())
