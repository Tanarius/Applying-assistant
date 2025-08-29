#!/usr/bin/env python3
"""
Debug GUI API Key Detection
============================

Comprehensive diagnostic to find why GUI is still showing instant mode
even after implementing API key detection.
"""

import sys
import os
from pathlib import Path

def test_import_paths():
    """Test all the import paths the GUI uses"""
    print("="*70)
    print("TESTING IMPORT PATHS")
    print("="*70)
    
    # GUI src path
    gui_src = Path(__file__).parent.parent / 'AUTOMATION-BOTS' / '05-AI-JOB-HUNT-COMMANDER' / 'src'
    print(f"GUI src path: {gui_src}")
    print(f"GUI src exists: {gui_src.exists()}")
    
    # Applying-assistant src path  
    applying_src = Path(__file__).parent / 'src'
    print(f"Applying-assistant src path: {applying_src}")
    print(f"Applying-assistant src exists: {applying_src.exists()}")
    
    # Add to Python path
    sys.path.append(str(applying_src))
    
    # Test imports
    try:
        from api_key_manager import find_openai_api_key
        print("✓ api_key_manager import successful")
    except Exception as e:
        print(f"✗ api_key_manager import failed: {e}")
        return False
        
    try:
        from main_application_engine import ApplicationEngine
        print("✓ main_application_engine import successful")
    except Exception as e:
        print(f"✗ main_application_engine import failed: {e}")
        return False
    
    return True

def test_api_key_detection():
    """Test API key detection system"""
    print("\n" + "="*70)
    print("TESTING API KEY DETECTION")
    print("="*70)
    
    # Add path
    sys.path.append(str(Path(__file__).parent / 'src'))
    
    try:
        from api_key_manager import find_openai_api_key
        
        print("1. Testing find_openai_api_key()...")
        api_key = find_openai_api_key()
        
        if api_key:
            print(f"   ✓ API key found: {api_key[:10]}...")
            return api_key
        else:
            print("   ✗ No API key found")
            
            # Check .env file specifically
            env_file = Path(__file__).parent / '.env'
            print(f"\n2. Checking .env file: {env_file}")
            print(f"   .env exists: {env_file.exists()}")
            
            if env_file.exists():
                with open(env_file, 'r') as f:
                    content = f.read()
                print(f"   .env content:")
                for i, line in enumerate(content.split('\n'), 1):
                    print(f"     {i}: {line}")
                    
                # Check for uncommented API key
                for line in content.split('\n'):
                    if line.startswith('OPENAI_API_KEY=') and not line.startswith('#'):
                        key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        print(f"   ✓ Found uncommented API key: {key[:10]}...")
                        return key
            
            return None
            
    except Exception as e:
        print(f"   ✗ API key detection failed: {e}")
        return None

def test_application_engine():
    """Test ApplicationEngine initialization"""
    print("\n" + "="*70)
    print("TESTING APPLICATION ENGINE")
    print("="*70)
    
    sys.path.append(str(Path(__file__).parent / 'src'))
    
    try:
        from main_application_engine import ApplicationEngine
        
        print("1. Initializing ApplicationEngine...")
        engine = ApplicationEngine(output_dir="test_debug")
        
        print(f"2. Engine created: {engine}")
        print(f"3. Has ai_mode attribute: {hasattr(engine, 'ai_mode')}")
        
        if hasattr(engine, 'ai_mode'):
            print(f"4. AI mode value: {engine.ai_mode}")
            if engine.ai_mode:
                print("   ✓ ENGINE IS IN AI MODE")
                return True
            else:
                print("   ✗ ENGINE IS IN TEMPLATE MODE")
                return False
        else:
            print("   ✗ Engine missing ai_mode attribute")
            return False
            
    except Exception as e:
        print(f"   ✗ ApplicationEngine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_openai_integration():
    """Test actual OpenAI integration"""
    print("\n" + "="*70)
    print("TESTING OPENAI INTEGRATION")  
    print("="*70)
    
    sys.path.append(str(Path(__file__).parent / 'src'))
    
    try:
        from api_key_manager import find_openai_api_key
        api_key = find_openai_api_key()
        
        if not api_key:
            print("   ✗ No API key - skipping OpenAI test")
            return False
            
        print(f"1. Using API key: {api_key[:10]}...")
        
        # Test OpenAI import
        try:
            import openai
            print("   ✓ OpenAI package imported")
        except ImportError:
            print("   ✗ OpenAI package not installed")
            print("   Run: pip install openai")
            return False
        
        # Test client creation
        try:
            client = openai.OpenAI(api_key=api_key)
            print("   ✓ OpenAI client created")
        except Exception as e:
            print(f"   ✗ OpenAI client creation failed: {e}")
            return False
        
        # Test API call
        try:
            print("   Testing API call...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'test successful'"}],
                max_tokens=5
            )
            result = response.choices[0].message.content
            print(f"   ✓ API call successful: {result}")
            return True
        except Exception as e:
            print(f"   ✗ API call failed: {e}")
            return False
            
    except Exception as e:
        print(f"   ✗ OpenAI integration test failed: {e}")
        return False

def main():
    """Run comprehensive diagnostics"""
    print("COMPREHENSIVE GUI API KEY DIAGNOSTICS")
    print("="*70)
    print("This will identify why the GUI is showing instant mode")
    print()
    
    # Test 1: Import paths
    imports_ok = test_import_paths()
    
    # Test 2: API key detection  
    api_key_found = test_api_key_detection()
    
    # Test 3: Application engine
    engine_ai_mode = test_application_engine()
    
    # Test 4: OpenAI integration
    openai_working = test_openai_integration()
    
    # Final diagnosis
    print("\n" + "="*70)
    print("FINAL DIAGNOSIS")
    print("="*70)
    
    if imports_ok and api_key_found and engine_ai_mode and openai_working:
        print("✓ ALL TESTS PASSED - GUI should be in AI mode")
        print("  If GUI still shows instant mode, there may be a GUI-specific issue")
    elif not imports_ok:
        print("✗ IMPORT ISSUE - GUI cannot import required modules")
    elif not api_key_found:
        print("✗ NO API KEY - Add OpenAI API key to .env file")
        print("  Edit: C:\\Users\\tanar\\Glyph\\Career Command Center\\applying-assistant\\.env")
        print("  Change: # OPENAI_API_KEY=sk-your-key-here")
        print("  To: OPENAI_API_KEY=sk-your-actual-api-key-here")
    elif not engine_ai_mode:
        print("✗ ENGINE IN TEMPLATE MODE - API key not being used by engine")
    elif not openai_working:
        print("✗ OPENAI API ISSUE - API key invalid or no credits")
    
    return imports_ok and api_key_found and engine_ai_mode and openai_working

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)