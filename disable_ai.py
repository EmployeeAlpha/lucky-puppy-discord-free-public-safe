\
import json
from pathlib import Path

CONFIG_FILE = Path("config.local.json")
EXAMPLE_FILE = Path("config.example.json")

if CONFIG_FILE.exists():
    cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
elif EXAMPLE_FILE.exists():
    cfg = json.loads(EXAMPLE_FILE.read_text(encoding="utf-8"))
else:
    cfg = {}

cfg["ai_enabled"] = False
CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
print("✅ AI has been DISABLED in private config.local.json.")
