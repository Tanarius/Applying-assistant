#!/usr/bin/env python3
"""
Simple Debug - Find GUI API Key Issue
"""

import sys
import os
from pathlib import Path

# Add path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

def main():
    print("SIMPLE API KEY DEBUG")
    print("="*50)
    
    # Test 1: Check .env file
    env_file = Path(__file__).parent / '.env'
    print(f"1. .env file: {env_file}")
    print(f"   Exists: {env_file.exists()}")
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        print("   Content:")
        for i, line in enumerate(content.split('\n'), 1):
            print(f"     {i}: {repr(line)}")
    
    # Test 2: API key detection
    try:
        from api_key_manager import find_openai_api_key
        print("\n2. API key detection:")
        api_key = find_openai_api_key()
        if api_key:
            print(f"   Found: {api_key[:10]}...")
        else:
            print("   Not found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Application engine
    try:
        from main_application_engine import ApplicationEngine
        print("\n3. Application engine test:")
        engine = ApplicationEngine(output_dir="test")
        print(f"   Has ai_mode: {hasattr(engine, 'ai_mode')}")
        if hasattr(engine, 'ai_mode'):
            print(f"   ai_mode value: {engine.ai_mode}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    main()