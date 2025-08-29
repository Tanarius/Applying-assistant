#!/usr/bin/env python3
"""
Test GUI API Detection - Debug why GUI still shows template mode
"""

import sys
from pathlib import Path

# Add the exact paths the GUI uses
gui_file = Path("C:/Users/tanar/Glyph/Career Command Center/AUTOMATION-BOTS/05-AI-JOB-HUNT-COMMANDER/gui/ai-job-hunt-commander-gui.py")
src_path = gui_file.parent.parent / 'src'
applying_assistant_src = gui_file.parent.parent.parent.parent / 'applying-assistant' / 'src'

sys.path.append(str(src_path))
sys.path.append(str(applying_assistant_src))

def test_gui_import():
    """Test if GUI can import the modules correctly"""
    print("GUI IMPORT TEST")
    print("="*50)
    
    try:
        from api_key_manager import find_openai_api_key
        print("✓ api_key_manager imported successfully")
        
        api_key = find_openai_api_key()
        if api_key:
            print(f"✓ API key found: {api_key[:10]}...")
        else:
            print("✗ No API key found")
            return False
            
    except Exception as e:
        print(f"✗ api_key_manager import failed: {e}")
        return False
    
    try:
        from main_application_engine import ApplicationEngine
        print("✓ main_application_engine imported successfully")
        
        # Test engine initialization exactly like GUI does
        engine = ApplicationEngine(output_dir="Generated_Applications")
        print(f"✓ Engine initialized")
        print(f"  Has ai_mode: {hasattr(engine, 'ai_mode')}")
        if hasattr(engine, 'ai_mode'):
            print(f"  ai_mode value: {engine.ai_mode}")
            return engine.ai_mode
        
    except Exception as e:
        print(f"✗ main_application_engine failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False

def main():
    print("TESTING GUI API DETECTION (EXACT GUI SIMULATION)")
    print("="*60)
    
    # Test with exact GUI paths and initialization
    ai_mode_detected = test_gui_import()
    
    if ai_mode_detected:
        print("\n✅ SUCCESS: GUI should detect AI mode")
        print("   If GUI still shows template mode, there may be a GUI refresh issue")
    else:
        print("\n❌ PROBLEM: GUI cannot detect AI mode")
        print("   This explains why GUI shows template mode")

if __name__ == "__main__":
    main()