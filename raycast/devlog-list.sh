#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title View Today's Dev Log
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📋
# @raycast.packageName Developer Tools

# Documentation:
# @raycast.description View all development logs for today
# @raycast.author wenzhengde
# @raycast.authorURL https://github.com/wenzhengde

DEVLOG_PATH="$HOME/.claude/skills/devlog/devlog.py"

# Run list with compact mode
python3 "$DEVLOG_PATH" list --compact
