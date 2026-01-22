#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Generate Daily Summary
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📝
# @raycast.packageName Developer Tools

# Documentation:
# @raycast.description Generate a summary of today's development work
# @raycast.author wenzhengde
# @raycast.authorURL https://github.com/wenzhengde

DEVLOG_PATH="$HOME/.claude/skills/devlog/devlog.py"

# Run daily summary with compact mode, AI summary, and clipboard copy
python3 "$DEVLOG_PATH" daily --compact --ai --copy
