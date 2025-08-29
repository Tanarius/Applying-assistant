#!/usr/bin/env python3
"""
Test GUI Paths - Debug where GUI is looking for .env file
"""

import sys
from pathlib import Path

def test_gui_paths():
    """Test the exact paths the GUI is using"""
    print("GUI PATH DEBUGGING")
    print("="*50)
    
    # Simulate GUI's path calculation
    gui_file = Path("C:/Users/tanar/Glyph/Career Command Center/AUTOMATION-BOTS/05-AI-JOB-HUNT-COMMANDER/gui/ai-job-hunt-commander-gui.py")
    print(f"GUI file location: {gui_file}")
    
    # GUI's src path calculation
    gui_src = gui_file.parent.parent / 'src'
    print(f"GUI src path: {gui_src}")
    print(f"GUI src exists: {gui_src.exists()}")
    
    # GUI's applying-assistant path calculation  
    applying_src = gui_file.parent.parent.parent.parent / 'applying-assistant' / 'src'
    print(f"GUI applying-assistant src path: {applying_src}")
    print(f"GUI applying-assistant src exists: {applying_src.exists()}")
    
    # Where GUI thinks .env file should be
    env_file_gui_path = applying_src.parent / '.env'
    print(f"GUI .env path: {env_file_gui_path}")
    print(f"GUI .env exists: {env_file_gui_path.exists()}")
    
    # Where .env file actually is
    actual_env = Path("C:/Users/tanar/Glyph/Career Command Center/applying-assistant/.env")
    print(f"Actual .env path: {actual_env}")
    print(f"Actual .env exists: {actual_env.exists()}")
    
    # Check if paths match
    paths_match = env_file_gui_path.resolve() == actual_env.resolve()
    print(f"Paths match: {paths_match}")
    
    if actual_env.exists():
        with open(actual_env, 'r') as f:
            content = f.read()
        print(f"\nActual .env content:")
        for i, line in enumerate(content.split('\n'), 1):
            print(f"  {i}: {repr(line)}")

if __name__ == "__main__":
    test_gui_paths()