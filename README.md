# 📝 Telegram To-Do Bot

A simple, self-hosted Telegram bot for managing your daily to-do list.

## Features
- Add, list, complete, and delete tasks
- Per-user task storage (SQLite)
- No webhook or domain required (long polling)
- Free deployment on Railway

## Commands
| Command | Description |
|---|---|
| /start | Welcome message |
| /add <task> | Add a new task |
| /list | Show all tasks |
| /done <id> | Mark task as done |
| /delete <id> | Delete a task |
| /clear | Remove all completed tasks |
| /help | Show help |

## Local Setup
1. Clone the repo
2. Install dependencies:
   pip install -r requirements.txt
3. Copy `.env.example` to `.env` and add your bot token from @BotFather
4. Run:
   export TELEGRAM_BOT_TOKEN=your_token
   python main.py

## Deploy on Railway
1. Push this repo to GitHub
2. Go to railway.app → New Project → Deploy from GitHub repo
3. Add environment variable: TELEGRAM_BOT_TOKEN = your token
4. Railway auto-deploys using the Procfile
5. Check Deployments → View Logs to confirm the bot is running

## Persistence Note
Railway containers reset on redeploy, so SQLite data is lost. For persistence:
- Add a Railway Volume mounted at /app, OR
- Migrate to Railway PostgreSQL for production use.

## License
MIT
