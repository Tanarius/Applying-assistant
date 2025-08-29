#!/usr/bin/env python3
"""
Quick API Key Setup Script
==========================
"""

import os
from pathlib import Path

def setup_api_key():
    """Setup OpenAI API key"""
    print("=" * 60)
    print("OPENAI API KEY SETUP")
    print("=" * 60)
    
    # Check if key already exists
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"+ API key found in environment: {api_key[:10]}...")
        return api_key
    
    # Check project .env
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY=' in content:
                print(f"+ API key found in {env_path}")
                return "found"
    
    print("X No API key detected")
    print("\nTo add your API key, create this file:")
    print(f"File: {env_path}")
    print("Content: OPENAI_API_KEY=your-key-here")
    
    # Create template .env file
    try:
        with open(env_path, 'w') as f:
            f.write("# Add your OpenAI API key here\n")
            f.write("# OPENAI_API_KEY=sk-your-key-here\n")
        print(f"\nCreated template file: {env_path}")
        print("Edit this file and uncomment the OPENAI_API_KEY line")
    except Exception as e:
        print(f"Could not create template: {e}")
    
    return None

if __name__ == "__main__":
    setup_api_key()