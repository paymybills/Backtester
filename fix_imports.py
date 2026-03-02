#!/usr/bin/env python3
"""Fix versioned imports in UI component files."""
import os
import re
from pathlib import Path

# Patterns to fix
patterns = [
    (r'"@radix-ui/([^"]+)@[0-9.]+', r'"@radix-ui/\1'),  # @radix-ui packages
    (r'"lucide-react@[0-9.]+', r'"lucide-react'),       # lucide-react
    (r'"class-variance-authority@[0-9.]+', r'"class-variance-authority'),  # cva
    (r'"react-day-picker@[0-9.]+', r'"react-day-picker'),  # day picker
]

ui_dir = Path("/home/moew/Documents/BacktestingEngine/ui/src/components/ui")
files_fixed = 0
replacements = 0

for tsx_file in ui_dir.glob("*.tsx"):
    content = tsx_file.read_text()
    original = content
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        tsx_file.write_text(content)
        files_fixed += 1
        replacements += content.count('"@radix-ui/') + content.count('"lucide-react"')
        print(f"Fixed: {tsx_file.name}")

print(f"\n✅ Fixed {files_fixed} files")
