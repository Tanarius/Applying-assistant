#!/usr/bin/env python3
"""
Validate AI Integration
======================

Tests the complete API key detection and AI integration pipeline
to ensure the system switches from template mode to AI mode properly.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from api_key_manager import find_openai_api_key, get_working_api_key
from main_application_engine import ApplicationEngine

def test_api_key_detection():
    """Test API key detection system"""
    print("="*70)
    print("API KEY DETECTION TEST")
    print("="*70)
    
    # Test find_openai_api_key function
    print("1. Testing find_openai_api_key()...")
    api_key = find_openai_api_key()
    
    if api_key:
        print(f"   + API key found: {api_key[:10]}...")
        print(f"   Key length: {len(api_key)} characters")
        print(f"   Starts with 'sk-': {api_key.startswith('sk-')}")
    else:
        print("   X No API key found")
        return False
        
    # Test OpenAI import and client creation
    print("\n2. Testing OpenAI client initialization...")
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        print("   + OpenAI client created successfully")
    except ImportError:
        print("   X OpenAI package not installed")
        print("   Run: pip install openai")
        return False
    except Exception as e:
        print(f"   X OpenAI client creation failed: {e}")
        return False
    
    # Test actual API call
    print("\n3. Testing OpenAI API call...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use cheaper model for testing
            messages=[
                {"role": "user", "content": "Say 'API test successful' if you receive this."}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"   + API call successful: {result}")
        return True
        
    except Exception as e:
        print(f"   X API call failed: {e}")
        if "insufficient_quota" in str(e).lower():
            print("   ! This usually means you need to add credits to your OpenAI account")
        elif "invalid_api_key" in str(e).lower():
            print("   ! Your API key appears to be invalid")
        return False

def test_application_engine_mode():
    """Test which mode the application engine uses"""
    print("\n" + "="*70)
    print("APPLICATION ENGINE MODE TEST")  
    print("="*70)
    
    try:
        print("Initializing ApplicationEngine...")
        engine = ApplicationEngine(output_dir="test_validation")
        
        # Check which mode it's in
        if hasattr(engine, 'ai_mode') and engine.ai_mode:
            print("+ APPLICATION ENGINE IS IN AI-POWERED MODE")
            print("   This means deep research will take 60-120 seconds")
            return True
        else:
            print("X APPLICATION ENGINE IS IN TEMPLATE MODE")
            print("   This means instant generation with basic templates")
            return False
            
    except Exception as e:
        print(f"X Application engine test failed: {e}")
        return False

def main():
    """Run complete validation"""
    print("AI INTEGRATION VALIDATION")
    print("="*70)
    
    # Step 1: API Key Detection
    api_working = test_api_key_detection()
    
    # Step 2: Application Engine Mode
    engine_ai_mode = test_application_engine_mode()
    
    # Final verdict
    print("\n" + "="*70)
    print("FINAL VALIDATION RESULTS")
    print("="*70)
    
    if api_working and engine_ai_mode:
        print("* VALIDATION SUCCESSFUL!")
        print("   Your system is configured for AI-POWERED mode")
        print("   Applications will use deep research and take 60-120 seconds")
        print("   Quality will be high with company-specific insights")
    elif api_working and not engine_ai_mode:
        print("! PARTIAL SUCCESS")
        print("   API key works but engine is in template mode")
        print("   There may be an integration issue")
    elif not api_working:
        print("X VALIDATION FAILED") 
        print("   API key is not working properly")
        print("   System will use template mode (instant, basic quality)")
        
        print("\n* TO FIX:")
        print("   1. Edit: C:\\Users\\tanar\\Glyph\\Career Command Center\\applying-assistant\\.env")
        print("   2. Change: # OPENAI_API_KEY=sk-your-key-here")
        print("   3. To: OPENAI_API_KEY=sk-your-real-key-here")
        print("   4. Remove the # and use your actual OpenAI API key")
        print("   5. Get API key from: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()