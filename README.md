```markdown
# IMDb Search Bot 🤖🎬

A Telegram bot for searching IMDb movie/TV information directly in chats. Features rich media responses and interactive results.

![MIT License](https://img.shields.io/badge/License-MIT-green.svg) [![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)

## Features ✨
- 🔍 Search IMDb titles by name, URL, or ID
- 🎞️ Detailed information with posters and trailers
- 🌐 Multi-language support
- 🔄 Interactive result selection
- 🤖 Automatic restarts on failure
- 📱 Responsive design for Telegram clients

## Installation 📦

### Clone Repository
```bash
git clone https://github.com/yourusername/IMDb-search-bot.git
cd IMDb-search-bot
```

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

## Configuration ⚙️

1. Copy the example configuration file:
```bash
cp config.example.py config.py
```

2. Edit `config.py` with your credentials:
```python
class Config:
    API_ID = "123456"          # Get from my.telegram.org
    API_HASH = "abcdef12345"   # Get from my.telegram.org
    BOT_TOKEN = "123:ABC"      # Get from @BotFather
    IMDB_TEMPLATE = """
    🏷 Title: {title} ({year})
    🌟 Rating: {rating}
    📖 Plot: {plot}
    """
```

## Deployment 🚀

### Systemd Service Setup

1. Create service file:
```bash
sudo nano /etc/systemd/system/imdb-bot.service
```

2. Paste this configuration (adjust paths as needed):
```ini
[Unit]
Description=IMDb Telegram Bot Service
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/IMDb-search-bot
ExecStart=/usr/bin/python3 /path/to/IMDb-search-bot/imdb_bot.py
Restart=always
RestartSec=30
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable imdb-bot
sudo systemctl start imdb-bot
```

## Service Management 🔧

| Command                      | Description                  |
|------------------------------|------------------------------|
| `sudo systemctl start imdb-bot` | Start the bot service       |
| `sudo systemctl stop imdb-bot`  | Stop the bot service        |
| `sudo systemctl restart imdb-bot` | Restart the bot service   |
| `journalctl -u imdb-bot -f`   | View live logs              |
| `systemctl status imdb-bot`   | Check service status        |

## Usage 🎯
Send these commands in Telegram:
```
/imdb The Matrix         # Search by title
/imdb tt0133093         # Search by IMDb ID
/imdb https://imdb.com  # Search by URL
```

## Directory Structure 📂
```
IMDb-search-bot/
├── config.py           # Configuration file
├── imdb_bot.py         # Main bot logic
├── requirements.txt    # Dependency list
└── imdb_bot.session    # Session file (auto-generated)
```

## License 📄
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Important Note:** Replace all placeholder credentials in `config.py` before deployment!  
**Maintainer Contact:** [@asifalex](https://t.me/asifalex) on Telegram
```
