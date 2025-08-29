#!/usr/bin/env python3
"""
Demo API Key Setup
==================

Shows you exactly what needs to be done to enable AI-powered mode.
"""

import os
from pathlib import Path

def show_api_key_status():
    """Show current API key detection status"""
    print("="*60)
    print("API KEY STATUS CHECK")
    print("="*60)
    
    # Check environment variable
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key:
        print(f"+ Environment Variable: {env_key[:10]}...")
    else:
        print("X Environment Variable: Not found")
    
    # Check .env file
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print(f"+ .env file exists: {env_file}")
        
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY=' in content and not content.startswith('#'):
                print("+ .env file contains API key")
            else:
                print("X .env file exists but no valid API key")
                
        print(f"\n.env file content:")
        print("-" * 30)
        print(content)
        print("-" * 30)
    else:
        print("X .env file: Not found")
    
    print("\nTO ENABLE AI-POWERED MODE:")
    print("1. Get API key from: https://platform.openai.com/api-keys")
    print(f"2. Edit this file: {env_file}")
    print("3. Change line to: OPENAI_API_KEY=sk-your-actual-key-here")
    print("4. Remove the # at the beginning")
    print("5. Save the file")
    print("6. Run the application again")
    
    print("\nEXPECTED RESULT:")
    print("- Template Mode (current): Instant results, basic quality")
    print("- AI Mode (with key): 60-120 seconds, high-quality research")

if __name__ == "__main__":
    show_api_key_status()