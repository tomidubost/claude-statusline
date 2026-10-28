#!/usr/bin/env bash
set -euo pipefail

DEST="$HOME/.claude/statusline-tokens.py"
SETTINGS="$HOME/.claude/settings.json"
RAW="https://raw.githubusercontent.com/tomidubost/claude-statusline/main/statusline-tokens.py"

mkdir -p "$HOME/.claude"
curl -fsSL "$RAW" -o "$DEST"
chmod +x "$DEST"

[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
cp "$SETTINGS" "$SETTINGS.bak"
python3 - "$SETTINGS" <<'PY'
import json, sys
path = sys.argv[1]
with open(path) as f:
    settings = json.load(f)
settings["statusLine"] = {
    "type": "command",
    "command": "~/.claude/statusline-tokens.py",
    "refreshInterval": 30,
}
with open(path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")
PY

echo "Listo. Reinicia Claude Code para ver la status line (respaldo en $SETTINGS.bak)."
