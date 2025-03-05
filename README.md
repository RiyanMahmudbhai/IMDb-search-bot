```markdown
# IMDb Search Bot 🤖🎬

A Telegram bot for searching IMDb movie/TV information directly in chats. Features rich media responses and interactive results.

## Features ✨
- IMDb title search by name/URL
- Detailed info with posters
- Interactive result selection
- Trailer links
- Multi-language support
- Automatic restarts

## Systemd Deployment 🚀

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/IMDb-search-bot.git
cd IMDb-search-bot
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Create Configuration
```bash
cp config.example.py config.py
nano config.py  # Add your credentials
```

### 4. Create Systemd Service
```bash
sudo nano /etc/systemd/system/imdb-bot.service
```

Paste this configuration (adjust paths if needed):
```ini
[Unit]
Description=IMDb Telegram Bot Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/IMDb-search-bot
ExecStart=/usr/bin/python3 /root/IMDb-search-bot/imdb_bot.py
Restart=always
RestartSec=30
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### 5. Enable & Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable imdb-bot
sudo systemctl start imdb-bot
```

### 6. Verify Operation
```bash
sudo systemctl status imdb-bot
journalctl -u imdb-bot -f  # Live logs
```

## Key Commands 🔧
- Start/Stop:  
  `sudo systemctl start|stop imdb-bot`
- Restart:  
  `sudo systemctl restart imdb-bot`
- Check Status:  
  `systemctl status imdb-bot`
- View Logs:  
  `journalctl -u imdb-bot -f`

## Configuration ⚙️
Edit `config.py` with:
```python
class Config:
    API_ID = "123456"          # From my.telegram.org
    API_HASH = "abcdef12345"   # From my.telegram.org
    BOT_TOKEN = "123:ABC"      # From @BotFather
    IMDB_TEMPLATE = """
    🏷 Title: {title} ({year})
    🌟 Rating: {rating}
    📖 Plot: {plot}
    """
```

## Usage 🎯
```
/imdb The Matrix         - Search movies
/imdb tt0133093         - Search by IMDb ID
/imdb https://imdb.com  - Search by URL
```

## Directory Structure 📂
```
IMDb-search-bot/
├── config.py           # Configuration
├── imdb_bot.py         # Main bot code
├── requirements.txt    # Dependencies
└── imdb_bot.session    # Auto-generated session
```

## License 📄
MIT License

---

**Note:** Replace placeholder credentials in config.py before deployment!  
**Maintainer:** Asif Alex (@asifalex)
```
