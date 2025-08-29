#!/usr/bin/env python3
"""
Test Fixed GUI - Verify the GUI now uses the updated engine
"""

import sys
from pathlib import Path

# Simulate exact GUI import process after fix
applying_assistant_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(applying_assistant_src))

gui_src = Path(__file__).parent.parent / 'AUTOMATION-BOTS' / '05-AI-JOB-HUNT-COMMANDER' / 'src'
sys.path.append(str(gui_src))

def main():
    print("TESTING FIXED GUI IMPORTS")
    print("="*50)
    
    try:
        from main_application_engine import ApplicationEngine
        from api_key_manager import find_openai_api_key
        print("+ Imports successful")
        
        # Test API key detection
        api_key = find_openai_api_key()
        print(f"+ API key found: {api_key[:10] if api_key else 'None'}...")
        
        # Test engine initialization (like GUI does)
        engine = ApplicationEngine(output_dir="Generated_Applications")
        print(f"+ Engine initialized")
        print(f"+ Has ai_mode: {hasattr(engine, 'ai_mode')}")
        
        if hasattr(engine, 'ai_mode'):
            print(f"+ ai_mode value: {engine.ai_mode}")
            if engine.ai_mode:
                print("SUCCESS: GUI will now show AI-POWERED MODE")
                return True
            else:
                print("PROBLEM: Engine still in template mode")
                return False
        else:
            print("PROBLEM: Engine missing ai_mode attribute")
            return False
            
    except Exception as e:
        print(f"- Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n** GUI SHOULD NOW DETECT AI MODE **")
        print("** Restart the GUI to see the change **")
    else:
        print("\n** GUI ISSUE PERSISTS **")