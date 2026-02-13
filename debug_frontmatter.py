#!/usr/bin/env python3
"""
Debug script to check frontmatter parsing
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path to import our modules
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from skills.file_processor import FileProcessor

# Create a test file similar to the one in the validation
test_content = """---
title: "Comprehensive Planning Request"
created: "2026-02-13T21:54:00"
status: "pending"
priority: "high"
action_required: "create_plan"
---

# Comprehensive Planning Request

## Business Objective
Launch a new product marketing campaign with multiple phases.
"""

# Write the test content to a file
test_file = Path("./AI_Employee_Vault/Needs_Action/DEBUG_test_frontmatter.md")
test_file.parent.mkdir(exist_ok=True)

with open(test_file, 'w', encoding='utf-8') as f:
    f.write(test_content)

print("Created test file with frontmatter:")
print(test_content)
print("="*50)

# Process the file
processor = FileProcessor()
parsed_data = processor._parse_file(test_file)

print("Parsed data:")
print(f"Frontmatter: {parsed_data.get('frontmatter', 'Not found')}")
print(f"Action determination: {processor._determine_action(parsed_data)}")

# Clean up
test_file.unlink()