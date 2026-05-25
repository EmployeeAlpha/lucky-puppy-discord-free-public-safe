# Lucky Puppy Discord Free

Public-safe version of the Lucky Puppy Discord bot.

## What this contains

- `bot.py` — local interactive Discord bot. Replies in DMs and when mentioned in any channel it can see.
- `post.py` — GitHub Actions scheduled poster for quotes/news.
- `quotes.txt` — 551 public quote lines, plus commented credit/footer notes.
- `config.example.json` — safe template only.
- `.env.example` — safe local environment template only.
- `.github/workflows/post-to-discord.yml` — scheduled Discord posting workflow.

## What must stay private

Never commit:

- `.env`
- `config.local.json`
- `config.json`
- Discord bot token
- Discord webhook URLs
- API keys

## Local bot setup

```powershell
cd C:\EmployeeAlpha\lucky-puppy-discord-free
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
notepad .env
python bot.py
```

## GitHub scheduled posting setup

Set GitHub repository secrets in:

`Settings -> Secrets and variables -> Actions -> New repository secret`

Common secrets:

- `DISCORD_WEBHOOK_URLS` — one webhook URL per line, for scheduled posts into multiple channels.
- `NEWS_API_KEY` — optional.
- Or, for bot-token posting:
  - `DISCORD_BOT_TOKEN`
  - `DISCORD_GUILD_ID`
  - `POST_TO_ALL_CHANNELS` = `true`

Use bot-token posting carefully. Webhook posting is safer for a public repository because the bot token stays away from GitHub Actions.
