#!/usr/bin/env python3
"""
Test script to verify .env file is loaded correctly
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import superclaude to trigger env loading
import superclaude

print("=" * 60)
print("Environment Variables Test")
print("=" * 60)

# Test environment variables from .env
env_vars = {
    "MORPH_API_KEY": "Morphllm API Key",
    "TAVILY_API_KEY": "Tavily API Key",
    "TWENTYFIRST_API_KEY": "21st.dev API Key",
}

all_found = True
for key, description in env_vars.items():
    value = os.getenv(key)
    if value:
        # Mask the key for security (show first 10 chars)
        masked = value[:10] + "..." if len(value) > 10 else value
        print(f"✓ {description:20} ({key}): {masked}")
    else:
        print(f"✗ {description:20} ({key}): NOT SET")
        all_found = False

print("=" * 60)
if all_found:
    print("✓ All environment variables loaded successfully!")
    print("\n.env file is working correctly.")
else:
    print("✗ Some environment variables are missing.")
    print("\nPlease check your .env file.")

print("=" * 60)
