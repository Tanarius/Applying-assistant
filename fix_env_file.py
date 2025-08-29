#!/usr/bin/env python3
"""
Fix .env File - Add OpenAI API Key
==================================

This script will help you properly configure the .env file for AI mode.
"""

import sys
from pathlib import Path

def show_current_status():
    """Show current .env file status"""
    env_file = Path(__file__).parent / '.env'
    
    print("CURRENT .ENV FILE STATUS")
    print("="*50)
    print(f"File: {env_file}")
    print(f"Exists: {env_file.exists()}")
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        
        print("\nCurrent content:")
        for i, line in enumerate(content.split('\n'), 1):
            print(f"  {i}: {line}")
        
        # Check for API key
        has_uncommented_key = any(
            line.startswith('OPENAI_API_KEY=') and not line.startswith('#')
            for line in content.split('\n')
        )
        
        if has_uncommented_key:
            print("\n✅ API key is properly configured")
            return True
        else:
            print("\n❌ API key is NOT properly configured (commented out or missing)")
            return False
    
    return False

def create_example_fix():
    """Create an example of how to fix the .env file"""
    print("\n" + "="*60)
    print("HOW TO FIX THE .ENV FILE")
    print("="*60)
    
    env_file = Path(__file__).parent / '.env'
    
    print(f"1. Edit this file: {env_file}")
    print("\n2. Change this line:")
    print("   # OPENAI_API_KEY=sk-your-key-here")
    print("\n3. To this (with your actual API key):")
    print("   OPENAI_API_KEY=sk-proj-your-actual-key-here")
    print("\n4. Key points:")
    print("   - Remove the # at the beginning")  
    print("   - Replace 'sk-your-key-here' with your real OpenAI API key")
    print("   - Your key should start with 'sk-proj-' or 'sk-'")
    print("   - Get your key from: https://platform.openai.com/api-keys")
    
    return str(env_file)

def test_after_fix():
    """Test if the fix worked"""
    print("\n" + "="*60)
    print("TESTING AFTER FIX")
    print("="*60)
    
    # Add to path and test
    sys.path.append(str(Path(__file__).parent / 'src'))
    
    try:
        from api_key_manager import find_openai_api_key
        api_key = find_openai_api_key()
        
        if api_key:
            print(f"✅ SUCCESS: API key detected: {api_key[:10]}...")
            print("✅ GUI will now show AI-POWERED MODE")
            return True
        else:
            print("❌ STILL NO API KEY: Please check your .env file edit")
            return False
            
    except Exception as e:
        print(f"❌ Error testing: {e}")
        return False

def main():
    """Main fix process"""
    print("OPENAI API KEY .ENV FILE FIXER")
    print("="*50)
    
    # Show current status
    is_configured = show_current_status()
    
    if is_configured:
        print("\n🎉 Your .env file is already properly configured!")
        test_after_fix()
    else:
        # Show how to fix
        env_path = create_example_fix()
        
        print(f"\n⚠️  MANUAL ACTION REQUIRED:")
        print(f"   1. Open: {env_path}")
        print(f"   2. Edit as shown above")
        print(f"   3. Save the file")
        print(f"   4. Restart the GUI")
        
        print(f"\n💡 After editing, run this script again to test:")
        print(f"   python {Path(__file__).name}")

if __name__ == "__main__":
    main()