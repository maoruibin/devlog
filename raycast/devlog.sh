#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Log Dev Work
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 📝
# @raycast.packageName Developer Tools
# @raycast.argument1 { "type": "dropdown", "placeholder": "Category", "data": [{"title": "🚨 Incident - 线上故障", "value": "incident"}, {"title": "✨ Feature - 业务需求", "value": "feat"}, {"title": "📐 Design - 技术方案", "value": "design"}, {"title": "🔧 Ops - 运维部署", "value": "ops"}, {"title": "🐛 Bug - 常规Bug", "value": "bug"}, {"title": "📚 Learn - 技术调研", "value": "learn"}, {"title": "📝 Misc - 其他", "value": "misc"}] }
# @raycast.argument2 { "type": "text", "placeholder": "Title (required)", "percentEncoded": false }
# @raycast.argument3 { "type": "text", "placeholder": "Detail (optional)", "optional": true, "percentEncoded": false }

# Documentation:
# @raycast.description Log development work with structured categorization
# @raycast.author wenzhengde
# @raycast.authorURL https://github.com/wenzhengde

DEVLOG_PATH="$HOME/.claude/skills/devlog/devlog.py"

# Get arguments
CATEGORY="$1"
TITLE="$2"
DETAIL="$3"

# Validate inputs
if [ -z "$CATEGORY" ] || [ -z "$TITLE" ]; then
    echo "❌ Error: Category and Title are required"
    exit 1
fi

# Run devlog with compact output
if [ -n "$DETAIL" ]; then
    python3 "$DEVLOG_PATH" "$CATEGORY" "$TITLE" -d "$DETAIL" --compact
else
    python3 "$DEVLOG_PATH" "$CATEGORY" "$TITLE" --compact
fi
