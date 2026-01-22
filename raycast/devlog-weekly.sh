#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Generate Weekly Report
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📊
# @raycast.packageName Developer Tools
# @raycast.argument1 { "type": "text", "placeholder": "Days (default: 7)", "optional": true }

# Documentation:
# @raycast.description Generate a weekly development report
# @raycast.author wenzhengde
# @raycast.authorURL https://github.com/wenzhengde

DEVLOG_PATH="$HOME/.claude/skills/devlog/devlog.py"
DAYS="${1:-7}"

# Run weekly with compact mode, AI summary, and clipboard copy
python3 "$DEVLOG_PATH" weekly --days "$DAYS" --compact --ai --copy
