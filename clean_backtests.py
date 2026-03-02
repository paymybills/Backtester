#!/usr/bin/env python3
"""
Script to clean NaN values from backtests.json
"""
import json
import math

def clean_nan_recursive(obj):
    """Recursively replace NaN and Inf with 0.0"""
    if isinstance(obj, dict):
        return {k: clean_nan_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_recursive(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return obj
    else:
        return obj

# Read the file
with open('data/backtests.json', 'r') as f:
    data = json.load(f)

# Clean all NaN values
cleaned_data = clean_nan_recursive(data)

# Write back
with open('data/backtests.json', 'w') as f:
    json.dump(cleaned_data, f, indent=2)

print(f"✓ Cleaned {len(cleaned_data)} backtests")
print("✓ All NaN and Inf values replaced with 0.0")
