#!/usr/bin/env python3
"""
OpenAI API Key Manager
=====================

Handles OpenAI API key detection and setup with multiple fallback options.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import os
import sys
from pathlib import Path
from typing import Optional

def find_openai_api_key() -> Optional[str]:
    """
    Find OpenAI API key from multiple sources:
    1. Environment variable OPENAI_API_KEY
    2. .env file in project directory
    3. .env file in user's home directory
    4. Manual input if none found
    """
    print("* Searching for OpenAI API key...")
    
    # Method 1: Environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"+ Found API key in environment variable: {api_key[:10]}...")
        return api_key
    
    # Method 2: .env file in project directory
    project_env = Path(__file__).parent.parent / ".env"
    if project_env.exists():
        api_key = _load_from_env_file(project_env)
        if api_key:
            print(f"+ Found API key in project .env file: {api_key[:10]}...")
            return api_key
    
    # Method 3: .env file in home directory
    home_env = Path.home() / ".env"
    if home_env.exists():
        api_key = _load_from_env_file(home_env)
        if api_key:
            print(f"+ Found API key in home .env file: {api_key[:10]}...")
            return api_key
    
    # Method 4: Manual input
    print("X No API key found in environment or .env files")
    return None

def _load_from_env_file(env_path: Path) -> Optional[str]:
    """Load API key from .env file"""
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"').strip("'")
    except Exception as e:
        print(f"! Could not read {env_path}: {e}")
    return None

def setup_api_key_interactively() -> Optional[str]:
    """Interactive API key setup"""
    print("\n" + "="*80)
    print("OPENAI API KEY SETUP")
    print("="*80)
    
    print("\nTo get deep AI-powered research (instead of instant templates):")
    print("1. Go to: https://platform.openai.com/api-keys")
    print("2. Create new secret key")
    print("3. Copy the key (starts with sk-)")
    print("\nCost: ~$0.50-2.00 per deep analysis (60-120 seconds)")
    print("Benefit: High-quality, personalized applications vs generic templates")
    
    choice = input("\nDo you want to enter your API key now? (y/n): ").lower().strip()
    
    if choice == 'y':
        api_key = input("\nPaste your OpenAI API key: ").strip()
        
        if api_key and api_key.startswith('sk-'):
            # Save to project .env file
            env_path = Path(__file__).parent.parent / ".env"
            try:
                with open(env_path, 'w') as f:
                    f.write(f"OPENAI_API_KEY={api_key}\n")
                print(f"\n✅ API key saved to {env_path}")
                print("🔄 Restart this program to use AI-powered generation")
                return api_key
            except Exception as e:
                print(f"⚠️ Could not save API key: {e}")
                print("You can manually set environment variable:")
                print(f"Windows: setx OPENAI_API_KEY \"{api_key}\"")
                return api_key
        else:
            print("❌ Invalid API key (should start with 'sk-')")
            return None
    else:
        print("\n📋 Using template mode (instant but basic quality)")
        print("To enable AI mode later, run: python api_key_manager.py")
        return None

def test_api_key(api_key: str) -> bool:
    """Test if API key is valid"""
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        print("🧪 Testing API key...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use cheaper model for testing
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API key test successful: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        print("Check your API key and account credits")
        return False

def get_working_api_key() -> Optional[str]:
    """Get and validate working API key"""
    
    # First try to find existing key
    api_key = find_openai_api_key()
    
    if api_key:
        # Test if it works
        if test_api_key(api_key):
            return api_key
        else:
            print("⚠️ Found API key but it's not working")
    
    # If no key found or key doesn't work, prompt for setup
    return setup_api_key_interactively()

def main():
    """Main function for interactive setup"""
    print("OpenAI API Key Manager - AI Job Hunt Commander")
    
    api_key = get_working_api_key()
    
    if api_key:
        print("\n🚀 Ready for AI-powered job applications!")
        print("Run: python ai_powered_application_engine.py")
    else:
        print("\n📋 Continuing with template mode")

if __name__ == "__main__":
    main()