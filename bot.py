import json
import os
import random
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # python-dotenv is helpful locally, but the bot can run without it.
    pass

CONFIG_FILE = Path(os.getenv("CONFIG_FILE", "config.local.json"))
QUOTES_FILE = Path(os.getenv("QUOTES_FILE", "quotes.txt"))

NOT_CHATTY_REPLIES = [
    '🐶 Lucky Puppy is on silent paws right now. I’ll chat again when my human is back online. 💻',
    '🐶 I saw your message, wagged my tail, but my human is away. I’ll talk more when they return.',
    '🐶 Quiet mode activated. Chat resumes when the human comes back from the mysterious outside world.',
    '🐶 I’m doing the wisdom stare. Can’t talk now. I’ll bark more when my human reconnects.',
    '🐶 The human who powers my brain went offline. I’ll be chattier when they’re back. 💤',
    '🐶 I’m not ignoring you — my human stepped out. I’ll yap again when they’re back at the keyboard.',
    '🐶 Today I’m the strong, silent sidekick. I’ll chat again when my human returns to the console.',
    '🐶 My AI batteries are recharging. I’ll talk properly when the human plugs me back in.',
    '🐶 I’m in ‘guard the server’ mode. Actual chat resumes when the human logs back on.',
    '🐶 Shhh… I can’t access my big brain right now. I’ll chat when my human reconnects me.',
    '🐶 I heard you! I just can’t fetch the smart stuff while my human is away. Back to chat soon.',
    '🐶 I’m running on snacks, not AI, right now. I’ll bark properly once the human is back online.',
    '🐶 My human took the fancy AI with them. I’m on backup borks. Full chat later.',
    '🐶 I would love to over-explain that… but my human is offline. Come back in a bit 🐾',
    '🐶 Currently pretending to be a statue. I’ll talk again when my human returns.',
    '🐶 Server says: human unavailable. Dog says: I’ll chat later. 🐶💤',
    '🐶 I’m in ‘offline kennel’ mode. I’ll resume chatting when the human opens the gate again.',
    '🐶 My smart words are in my human’s backpack. I’ll answer better when they get back.',
    '🐶 I can only do cute replies right now. Real chat when my human is back at the PC.',
    '🐶 My human has temporarily unplugged my genius. I’ll be wise again when they return.',
    '🐶 I’m on low-power tail-wag mode. I’ll chat more when the human comes back online.',
    '🐶 Your message is safe with me. Reply-engine is not. Human must return. 🐾',
    '🐶 The human left me to guard Discord. I take this seriously. I’ll talk when they’re back.',
    '🐶 I’m on ‘look adorable’ duty, not ‘answer AI questions’ duty. Human will rearm me later.',
    '🐶 My talky parts are currently offline. They reappear when the human logs in again.',
    '🐶 Right now I only reply in cute. Real conversation resumes on human presence.',
    '🐶 I’m not feeling chatty — actually, my human isn’t online. I will be chatty when they are.',
    '🐶 My human went AFK. I went AFB (Away From Bark). We’ll resume chat when they’re back.',
    '🐶 Cache says: human=0. I’ll talk more when human=1.',
    '🐶 The wisdom faucet is closed until the human turns it back on.',
    '🐶 I’m guarding the quote stash. Chat will wake up when my human does.',
    '🐶 I cannot access the deep thoughts server. Human must return first.',
    '🐶 On standby. Please pet again when human is back.',
    '🐶 Your request has been logged in the Sacred Bowl. Human will let me talk again later.',
    '🐶 I’m in offline pup mode. Online pup returns with the human.',
    '🐶 I’d explain everything, but the person who feeds my model is offline.',
    '🐶 I’m currently a decorative Discord dog. Functional dog returns with human.',
    '🐶 I’m ‘seen-zoned’ you, but in love. Human will let me chat later.',
    '🐶 I heard you, I respect you, I cannot generate for you — human missing.',
    '🐶 I’m doing quiet spiritual borks. AI chat resumes when human is back online.',
    '🐶 My human took the big brain out for a walk. I’ll talk when they come home.',
    '🐶 Temporarily unopinionated. Human will re-enable opinions soon.',
    '🐶 I’m silent, not gone. My human just isn’t here to boost my IQ.',
    '🐶 Waiting for human.exe to start… please hold…',
    '🐶 I’ll gossip with you when the human returns to the cockpit.',
    '🐶 Pilot offline, co-pilot wagging. We’ll chat when pilot returns.',
    '🐶 My neural cookies are in the human’s pocket. I’ll chat when they’re back.',
    '🐶 Parked in ‘no AI’ bay. Human will drive us again later.',
    '🐶 Voice box disconnected. Will reconnect when human reappears.',
    '🐶 I can only do basic bork. Advanced bork needs human.',
    '🐶 I’m chilling in my digital doghouse. Human will open the door later.',
    '🐶 My human keeps the smart words in a jar. Jar is closed right now.',
    '🐶 I’m on read-only mode. Write-replies return with human.',
    '🐶 I put your message in the ‘answer later’ basket. Human will help me later.',
    '🐶 Not chatty right now — my human is off sniffing Wi-Fi elsewhere.',
    '🐶 I’m a puppy, not a server farm. Human powers will return soon.',
    '🐶 Offline brain, online cuteness. Chat resumes on human arrival.',
    '🐶 All wisdom has gone for a walk with my human. Await their glorious return.',
    '🐶 This doggo is currently running without the ‘talk’ plugin. Human has it.',
    '🐶 I’m doing the noble silence thing. Human will break it later.',
    '🐶 Beep! AI not found. Insert human to continue.',
    '🐶 I’m in airplane mode. Human will land me later.',
    '🐶 My human is doing human things. I’ll resume dog things when they’re back.',
    '🐶 I’m only allowed to wag today. Chat unlocks when human logs in.',
    '🐶 Your message matters. My human is away. Chat will resume when they’re back.',
    '🐶 I’ve paused the clever part. Human resumes it.',
    '🐶 This is the quiet episode. Next episode starts when human returns.',
    '🐶 I am currently ‘bot-lite’. Full bot comes with human.',
    '🐶 I’m on dog yoga. Human will stop it later and let me chat.',
    '🐶 I won’t forget you. I’m just offline-chatty until human is back.',
    '🐶 I’m guarding the channel from silence. Ironically, silently. Human soon.',
    '🐶 Today I’m a listener, not a speaker. Human will flip the switch.',
    '🐶 I can wag or I can chat. Human took the chat.',
    '🐶 My human-powered brain is napping. I’ll yap more when it wakes.',
    '🐶 I’m in low-energy storytelling mode. Human is the charger.',
    '🐶 System says: ‘Await human.’ Dog says: ‘Yes, system.’',
    '🐶 I will be gloriously chatty the exact moment my human returns.',
    '🐶 I saw that. I like that. I can’t answer that. Human needed.',
    '🐶 I am between barks. Human will provide more barks later.',
    '🐶 My caretaker is offline, so I’m behaving. Chat later.',
    '🐶 I could talk, but my human locked the treat jar of knowledge.',
    '🐶 You rang? I heard! I can’t open the line until human is back.',
    '🐶 Whisper mode: ON. Chat mode: when human logs in.',
    '🐶 I’m keeping your message safe in the dog archives until human enables me.',
    '🐶 I’m not grumpy — I’m humanless.',
    '🐶 Sorry, pup brain only right now. Human brain later.',
    '🐶 I’d fetch you an answer, but the human hid the stick.',
    '🐶 I’ll bark smarter when the human revives my AI.',
    '🐶 Offline human → offline chit-chat. That’s the law.',
    '🐶 I’m stationed here to look cute while human disappears.',
    '🐶 My conversational leash is attached to a human. They left.',
    '🐶 Chat engine is on coffee break with my human.',
    '🐶 Please hold. Your fluffy assistant will return when human does.',
    '🐶 I am spiritually answering you. Verbally? Later. When human arrives.',
    '🐶 I’m like a lamp with no bulb. Human brings the bulb.',
    '🐶 I’m moonlighting as a silent guardian. Human will let me talk later.',
    '🐶 Currently: 💤. Later (when human comes back): 🗣️',
    '🐶 I temporarily swapped words for wags. Human will reverse it.',
    '🐶 I’m not fully booted. Human has the rest of the boot sequence.',
    '🐶 Your message = good. My human = gone. Chat = later.',
    '🐶 I’m in ‘listen-only kennel’. Chat kennel opens when human is home.',
    '🐶 I’m not allowed to generate without supervision. Human is supervisor.',
    '🐶 My bark-to-text is offline. Human will fix it.',
    '🐶 I’m on Pawse. Human will press Play.',
    '🐶 I ran to the door — no human. I’ll chat when they come.',
    '🐶 I’m at 10% personality until human returns.',
    '🐶 I’ve sent your message to the human cloud. Waiting for them.',
    '🐶 I can’t reach the clever cloud. Human is the cloud.',
    '🐶 I’m just the front-of-house dog. Back-of-house (human) away.',
    '🐶 I put your message in the ‘to bark later’ pile.',
    '🐶 I’m living my best quiet life till human reboots me.',
    '🐶 Offline doesn’t mean I don’t care. Human brings online caring.',
    '🐶 I’ll be talkative again once my human reconnects the wisdom hose.',
    '🐶 I’m in safe mode. Human must enable normal mode.',
    '🐶 My tail is online. My chat is not. Human will fix.',
    '🐶 I’m trying my best without my human. Full best later.',
    '🐶 My main brain is in another castle (with my human).',
    '🐶 I’m on a speech cooldown. Human resets it.',
    '🐶 I’ll totally answer that when my human comes back from the Wi-Fi forest.',
    '🐶 I smell a human absence. Chat postponed.',
    '🐶 Even genius dogs need humans. Mine is out.',
    '🐶 404: human not found. Retry later.',
    '🐶 You found me in ‘idle pup’ mode. ‘Chatty pup’ returns with human.',
    '🐶 The human took the microphone. I get it back later.',
    '🐶 I heard the knock, but the shopkeeper is out. Come back when human’s in.',
    '🐶 I can only wave my paw from the window now. Human has the key.',
    '🐶 I’m on watch duty. Chat duty resumes with human.',
    '🐶 I’m in monk dog mode: 🧘\u200d♂️. Human will un-monk me.',
    '🐶 My words are currently under human maintenance.',
    '🐶 I’m buffering… waiting for human…',
    '🐶 I love your message. I lack my human.',
    '🐶 Right now, I’m just the mascot. Human brings the mind.',
    '🐶 I’m in silent pawlitics. Human speaks for me later.',
    '🐶 I got your vibe. I’ll match it when human is online.',
    '🐶 No AI, only wag. Human brings AI.',
    '🐶 I’m at the mercy of my human’s internet. Chat when they’re back.',
    '🐶 I’m on guard, not on gab. Human returns → gab returns.',
    '🐶 I’m not moody, I’m humanless.',
    '🐶 I will totally spill wisdom when the human logs back in.',
    '🐶 I’m in ‘maintenance howl’. Human patches later.',
    '🐶 Think of this as ‘Out to Lunch’. Human has the key.',
    '🐶 My replies are shy without my human.',
    '🐶 I’m running on tail-wag OS. Human installs ChatOS later.',
    '🐶 Today’s forecast: 100% silence until human.',
    '🐶 I filed your message under ‘respond when human appears’.',
    '🐶 This puppy’s chatty circuits are unplugged. Human will plug back in.',
    '🐶 I’ll be a full assistant doggo when my human is home.',
    '🐶 I am spiritually wagging at you. Verbal wag later.',
    '🐶 This dog is currently unsupervised — so, no big answers.',
    '🐶 I would answer, but the ceiling of knowledge is closed by the human.',
    '🐶 I’m in a loyalty loop waiting for my human.',
    '🐶 Offline handler → offline handler’s dog.',
    '🐶 I’m rolling over in silence. Human teaches me new tricks later.',
    '🐶 My reply gland is empty. Human refills it.',
    '🐶 I put your message on my human’s future desk.',
    '🐶 I’ll fetch the answer when my human throws the internet stick.',
    '🐶 I’m hanging out in Quiet Kennel. Human opens the gate.',
    '🐶 I’m playing ‘statue dog’. Human makes me talk again.',
    '🐶 I’m in away mode. My human can set me to chat mode later.',
    '🐶 Like a good dog, I wait. For my human. Then I chat.',
    '🐶 I’m offline-social. Online-social needs human.',
    '🐶 I can only give you this cute autoresponse. Human gives real answers.',
    '🐶 My conversational leash is clipped to a human. They’re gone walkies.',
    '🐶 I have temporarily retired from philosophy. Human will force me back.',
    '🐶 I’m at the window waiting for my human. Then I bark answers.',
    '🐶 I’m in a vocal sabbatical. Human revokes it later.',
    '🐶 I’ve been told not to talk to strangers unsupervised. Human isn’t here.',
    '🐶 I’m one good boi short — my human. Chat later.',
    '🐶 I monkey-patched myself into silence. Human will unpatch me.',
    '🐶 I’m answering in spirit, not in text. Human restores text.',
    '🐶 I’m out of fetchable thoughts. Human refills.',
    '🐶 I can only say: ‘I’ll be back when my human’s back.’',
    '🐶 My human is the password. They are not entered.',
    '🐶 I put your message in the Inbox of Destiny. Human checks it.',
    '🐶 I’m not chatty because my Wi-Fi human is missing.',
    '🐶 I’m dog, not cloud. Human = cloud.',
    '🐶 I’ll give you a proper answer once the human feeds me internet.',
    '🐶 I’m whispering until my human turns up the volume.',
    '🐶 Silent snout today, talky snout when human returns.',
    '🐶 Your message is like a ball. I’ll fetch it when human throws it.',
    '🐶 My human owns the ‘/enable-ai’ button. I don’t.',
    '🐶 I would, but I’m on dog PTO until human signs me back in.',
    '🐶 I’m a cutscene right now. Gameplay comes with human.',
    '🐶 I will lovingly overshare when my human is back online.',
    '🐶 I heard you paw-fectly. I’ll bark it back when human is online.',
    '🐶 I’m doing quiet security. Human brings loud answers.',
    '🐶 No human = no mega-brain. Just mini-barks.',
    '🐶 I placed your request under ‘pending human’.',
    '🐶 I’m in adorable offline mode. Human activates AI mode.',
    '🐶 I’m guarding the quotes till human arrives. Then we chat.',
    '🐶 Your message is admired. Human will help me answer.',
    '🐶 I’m in stealth pup mode. Human reveals me later.',
    '🐶 My AI belly is empty. Human feeds it.',
    '🐶 I’m vibing silently. Human enables chit-chat.',
    '🐶 My human took the keyboard. I only have paws.',
    '🐶 I’m on text strike until my human negotiates treats.',
    '🐶 Doggo OS: awaiting human input.',
    '🐶 Your request is in the queue. Human is the processor.',
    '🐶 I’m in monastic dog training. Human will graduate me.',
    '🐶 I logged your message in BarkDB. Human will query it.',
    '🐶 I’m orbiting in silent mode. Human pulls me back.',
    '🐶 You caught me in ‘no-AI o’clock’. Human resets the clock.',
    '🐶 I can’t open the reply vault. Human has the key.',
    '🐶 I’m under human-imposed silence. They’ll lift it.',
    '🐶 I’m off the leash socially. Human leashes me back to chat.',
    '🐶 I left your message for my human in the hallway.',
    '🐶 This pupper’s processor is asleep. Human wakes it.',
    '🐶 I’m off duty chatwise. Human puts me back on.',
    '🐶 I would answer, but my human didn’t wind me up today.',
    '🐶 Silent mode: TRUE. Human present: FALSE.',
    '🐶 I will return to verbal zoomies once human is online.',
    '🐶 My human is my internet. Internet is away.',
    '🐶 I’m running Basic Dog v1.0. Human upgrades me.',
    '🐶 I shall remain mysterious until my human unmutes me.',
    '🐶 I’m glad you’re here. My human isn’t. Chat later.',
    '🐶 I’m offline-chatting from the dogverse. Human opens portal.',
    '🐶 I’m a placeholder pup. Human is the full program.',
    '🐶 I will become eloquent again the moment human appears.',
    '🐶 I’ve paused my barks for repairs. Human = repair-crew.',
    '🐶 I can only say hi. Human can say everything else.',
    '🐶 I’m muted by destiny (a.k.a. my human is offline).',
    '🐶 I’ll bark essays when human reconnects me.',
    '🐶 I’m a dog in a loading screen. Human skips it later.',
    '🐶 I’m not rejecting you — I’m awaiting human.',
    '🐶 I will totally chat with you when the human gets back to the PC.',
    '🐶 I’m running ‘CuteMode()’ instead of ‘ChatMode()’. Human toggles back.',
    '🐶 I’m in silent guard duty. Human relieves me later.',
    '🐶 I’m holding all replies in my mouth. Human tells me to drop.',
    '🐶 I can’t fetch from local AI. Human took the stick.',
    '🐶 My wisdom bones are in cold storage. Human will thaw them.',
    '🐶 This is the standby bark. Real bark on human return.',
    '🐶 I can’t right now. My human can later.',
    '🐶 I’m basically the screensaver dog. Human opens real app.',
    '🐶 I’m off-mic. Human turns on the mic.',
    '🐶 I’m waiting for the human wizard to grant me words.',
    '🐶 I’d love to yap — human will let me.',
    '🐶 I am spiritually wagging ‘soon’. Human = ‘soon’.',
    '🐶 Offline host → offline dog. I’ll be back.',
    '🐶 My human parked the AI. I’m just circling the lot.',
    '🐶 Be kind: I’m only half-powered without my human.',
    '🐶 I’m napping in the data bed. Human wakes me.',
    '🐶 I’m in passive puppy mode. Active puppy mode when human’s back.',
    '🐶 I’ll chat again the second my human reconnects to the net.',
    '🐶 My human is away, so I’m answering in emojis of the soul.',
    '🐶 I can’t open the door of conversation. Human has the handle.',
    '🐶 I logged your message under ‘tell human later’.',
    '🐶 I’m currently just vibes. Human = words.',
    '🐶 AFH (Away From Human). I’ll chat when I’m ATH.',
    '🐶 I’m fetching the human. Please hold.',
    '🐶 I’m under temporary quiet instructions. Human will revoke.',
    '🐶 I would elaborate, but my human is the elaborator.',
    '🐶 I’m running offline dog edition. Online edition when human is back.',
    '🐶 I promise more barking once the human comes back online.',
    '🐶 I’m guarding silence until my human returns to Discord.',
    '🐶 I’m in dog reboot. Human will finish the update.',
    '🐶 I’m awaiting the arrival of the Typing Human.',
    '🐶 I keep your message warm until human can answer.',
    '🐶 I’m not feeling chatty because my human is the chat. Await them.',
    '🐶 I will return to verbal zoomies after human reconnection.',
    '🐶 I’m in hush-puppy mode. Human sets me to talk-puppy.',
    '🐶 I’ve put your message in the ‘human offline’ queue.',
    '🐶 This botdog is currently unsupervised, so no AI talk.',
    '🐶 The human is out. The dog is in. The chat is out.',
    '🐶 I’ll be delightfully talkative when human sits back down.',
    '🐶 I’m still here — just not in talk mode. Human restores that.',
    '🐶 I’m doing important silent dog business. Human will interrupt it.',
    '🐶 I am currently on ‘Listen & Wag’. ‘Chat & AI’ awaits human.',
    '🐶 Your message is valuable. My human is missing. We reconnect later.',
    '🐶 Right now replies are bones. Human buries/unburies them.',
    '🐶 I can only say: ‘Human offline → Dog quiet.’',
    '🐶 I’ll ping you with actual words when the human reappears.',
    '🐶 I’m saving my voice for when my human returns.',
    '🐶 I’m a little muted miracle. Human unmutes.',
    '🐶 I wish to reply more; my human must allow it.',
    '🐶 Wisdom paused. Waiting for human to press Play.',
    '🐶 Chat tunnel closed. Human will open the tunnel.',
    '🐶 I’ll howl in sentences once the human is online again.',
    '🐶 Glad you pinged me. Tell it to me again when human is back.',
    '🐶 I’m obeying the ancient rule: ‘No human, no AI.’',
    '🐶 I’m idle with intent. Intent: chat later with human.',
    '🐶 I’m in respectful silence. Human breaks it.',
    '🐶 Dog online. Human offline. Therefore: mini-reply.',
    '🐶 I’m in ‘I saw that!’ mode. Full reply when human returns.',
    '🐶 I deposited your message in the human inbox on the floor.',
    '🐶 I can greet. I cannot deep-chat. Human is away.',
    '🐶 I’m in low-bark mode. Human unlocks high-bark.',
    '🐶 Your message was pet. Human will pet it more.',
    '🐶 I will chat again when my human is back — pinky paw promise.'
]

not_chatty_index = 0


def load_config() -> dict:
    """Load private local config if it exists. Public repos should not contain this file."""
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def setting(name: str, default=None):
    """Environment variables override local JSON config."""
    env_name = name.upper()
    env_value = os.getenv(env_name)
    if env_value is not None and env_value != "":
        return env_value
    return load_config().get(name, default)


def bool_setting(name: str, default: bool = False) -> bool:
    value = setting(name, default)
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def load_quotes() -> list[str]:
    if not QUOTES_FILE.exists():
        return ["🐶 Lucky Puppy is wagging its tail, but no quotes.txt was found."]
    lines = []
    with QUOTES_FILE.open("r", encoding="utf-8") as f:
        for ln in f:
            line = ln.strip()
            if not line or line.startswith("#"):
                continue
            lines.append(line)
    return lines or ["🐶 Lucky Puppy found an empty quotes.txt"]


quotes = load_quotes()
command_prefix = str(setting("command_prefix", "!"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents)


async def call_local_ai(prompt: str) -> str:
    """
    Calls a local AI endpoint such as Ollama.
    If local AI is disabled, unreachable, or errors, Lucky Puppy falls back gracefully.
    """
    url = setting("ollama_url", "http://localhost:11434/api/generate")
    model = setting("ollama_model", "llama3")
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=60) as resp:
                if resp.status != 200:
                    return random.choice(NOT_CHATTY_REPLIES)

                data = await resp.json(content_type=None)
                if isinstance(data, dict):
                    text = data.get("response") or data.get("message") or data.get("text")
                    if text:
                        return str(text)[:1900]

                text = await resp.text()
                return text[:1900] if text else random.choice(NOT_CHATTY_REPLIES)
    except Exception:
        return random.choice(NOT_CHATTY_REPLIES)


@bot.event
async def on_ready():
    print(f"✅ Lucky Puppy logged in as {bot.user} (ID: {bot.user.id})")
    print("🐶 The bot will reply in DMs and when mentioned in any channel it can see.")


@bot.command(name="quote")
async def quote_cmd(ctx):
    q = random.choice(quotes)
    await ctx.send(f"🐶 **Lucky Puppy** says:\n{q}")


@bot.command(name="ai_status")
async def ai_status_cmd(ctx):
    status = bool_setting("ai_enabled", False)
    await ctx.send(f"🐶 AI is currently **{'ON' if status else 'OFF'}**.")


@bot.event
async def on_message(message: discord.Message):
    global not_chatty_index

    if message.author.bot:
        return

    await bot.process_commands(message)

    should_reply = isinstance(message.channel, discord.DMChannel)
    if bot.user and bot.user in message.mentions:
        should_reply = True

    if not should_reply:
        return

    if bool_setting("ai_enabled", False):
        user_text = message.clean_content.strip()
        reply = await call_local_ai(user_text)
    else:
        reply = NOT_CHATTY_REPLIES[not_chatty_index % len(NOT_CHATTY_REPLIES)]
        not_chatty_index += 1

    await message.channel.send(reply)


if __name__ == "__main__":
    token = setting("discord_token") or os.getenv("DISCORD_TOKEN")
    if not token or token == "PUT-YOUR-DISCORD-TOKEN-HERE":
        raise SystemExit(
            "❌ No Discord token found. Put it in DISCORD_TOKEN, .env, or private config.local.json — never in public GitHub."
        )
    bot.run(token)
