\
import os
import random
from pathlib import Path

import requests

QUOTES_FILE = Path("quotes.txt")
INDEX_FILE = Path("next_index.txt")

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
DISCORD_WEBHOOK_URLS = os.getenv("DISCORD_WEBHOOK_URLS", "").strip()

# Optional bot-token mode. Use only through GitHub Secrets, never hardcoded.
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
DISCORD_CHANNEL_IDS = os.getenv("DISCORD_CHANNEL_IDS", "").strip()
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID", "").strip()
POST_TO_ALL_CHANNELS = os.getenv("POST_TO_ALL_CHANNELS", "false").strip().lower() in ("1", "true", "yes", "on")

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()  # optional


def split_secret_list(raw: str) -> list[str]:
    if not raw:
        return []
    items = []
    for line in raw.replace(",", "\n").splitlines():
        item = line.strip()
        if item:
            items.append(item)
    return items


def load_quotes() -> list[str]:
    if not QUOTES_FILE.exists():
        return ["🐶 Lucky Puppy couldn’t find quotes.txt"]
    lines = []
    with QUOTES_FILE.open("r", encoding="utf-8") as f:
        for ln in f:
            line = ln.strip()
            if not line or line.startswith("#"):
                continue
            lines.append(line)
    return lines or ["🐶 No quotes available."]


def load_index() -> int:
    if not INDEX_FILE.exists():
        return 0
    txt = INDEX_FILE.read_text(encoding="utf-8").strip()
    return int(txt) if txt.isdigit() else 0


def save_index(i: int) -> None:
    INDEX_FILE.write_text(str(i), encoding="utf-8")


def fetch_news() -> str | None:
    # Optional GNews mode. If no key exists, use a neutral public link fallback.
    if NEWS_API_KEY:
        url = f"https://gnews.io/api/v4/top-headlines?token={NEWS_API_KEY}&lang=en&max=3"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            articles = data.get("articles", [])
            if articles:
                lines = []
                for article in articles[:3]:
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "source")
                    lines.append(f"• {title} ({source})")
                return "📰 *Today’s Headlines:*\n" + "\n".join(lines)
        except Exception as exc:
            print(f"⚠️ News fetch failed: {exc}")

    return "📰 Latest world news: https://www.reuters.com/world/"


def build_message() -> str:
    quotes = load_quotes()
    idx = load_index()
    quote = quotes[idx % len(quotes)]
    news = fetch_news()

    msg = f"🐶 **Lucky Puppy** says:\n{quote}"
    if news:
        msg += "\n\n" + news

    save_index((idx + 1) % len(quotes))
    return msg[:1900]


def send_webhook(url: str, msg: str) -> None:
    r = requests.post(url, json={"content": msg}, timeout=15)
    r.raise_for_status()


def discord_api(method: str, endpoint: str, **kwargs):
    if not DISCORD_BOT_TOKEN:
        raise RuntimeError("DISCORD_BOT_TOKEN not set")
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bot {DISCORD_BOT_TOKEN}"
    headers["Content-Type"] = "application/json"
    r = requests.request(method, f"https://discord.com/api/v10{endpoint}", headers=headers, timeout=20, **kwargs)
    if r.status_code >= 400:
        raise RuntimeError(f"{method} {endpoint} failed: {r.status_code} {r.text[:300]}")
    if r.text:
        return r.json()
    return None


def get_all_text_channel_ids() -> list[str]:
    if not DISCORD_GUILD_ID:
        raise RuntimeError("DISCORD_GUILD_ID is required when POST_TO_ALL_CHANNELS=true")
    channels = discord_api("GET", f"/guilds/{DISCORD_GUILD_ID}/channels")
    # 0 = Guild Text, 5 = Guild Announcement. Avoid forums/threads/stages/voice.
    return [str(ch["id"]) for ch in channels if ch.get("type") in (0, 5)]


def send_bot_message(channel_id: str, msg: str) -> None:
    discord_api("POST", f"/channels/{channel_id}/messages", json={"content": msg})


def main():
    msg = build_message()
    sent = 0

    webhook_urls = []
    if DISCORD_WEBHOOK_URL:
        webhook_urls.append(DISCORD_WEBHOOK_URL)
    webhook_urls.extend(split_secret_list(DISCORD_WEBHOOK_URLS))

    for url in webhook_urls:
        try:
            send_webhook(url, msg)
            sent += 1
        except Exception as exc:
            print(f"❌ Webhook post failed: {exc}")

    channel_ids = split_secret_list(DISCORD_CHANNEL_IDS)
    if POST_TO_ALL_CHANNELS:
        channel_ids.extend(get_all_text_channel_ids())

    seen = set()
    for channel_id in channel_ids:
        if channel_id in seen:
            continue
        seen.add(channel_id)
        try:
            send_bot_message(channel_id, msg)
            sent += 1
        except Exception as exc:
            print(f"❌ Bot post failed for channel {channel_id}: {exc}")

    if sent == 0:
        raise SystemExit("❌ No Discord target configured. Set DISCORD_WEBHOOK_URLS, DISCORD_WEBHOOK_URL, or bot-token channel settings.")

    print(f"✅ Posted Lucky Puppy message to {sent} Discord target(s).")


if __name__ == "__main__":
    main()
