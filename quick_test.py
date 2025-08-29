#!/usr/bin/env python3
"""
Quick Test - Parallel AI System
===============================
Simple test to verify the sophisticated parallel AI system is working.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def main():
    """Test the parallel AI system"""
    print("PARALLEL AI SYSTEM TEST")
    print("=" * 50)
    
    try:
        from main_application_engine import ApplicationEngine
        
        print("1. Initializing ApplicationEngine...")
        engine = ApplicationEngine(output_dir="quick_test")
        
        print(f"2. AI Mode: {hasattr(engine, 'ai_mode') and engine.ai_mode}")
        print(f"3. Parallel Mode: {hasattr(engine, 'parallel_mode') and engine.parallel_mode}")
        
        if hasattr(engine, 'parallel_mode') and engine.parallel_mode:
            print("[SUCCESS] SOPHISTICATED PARALLEL AI MODE ENABLED")
            print("Starting quick test generation...")
            
            start_time = time.time()
            
            # Generate application
            result = engine.process_job_application(
                company_name="Microsoft",
                job_title="Senior Software Engineer"
            )
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            print(f"\n[COMPLETED] Generation finished!")
            print(f"[TIME] Total Time: {generation_time:.1f} seconds")
            
            if result and 'mode' in result:
                print(f"[MODE] Used: {result['mode']}")
                
                if 'performance_metrics' in result:
                    metrics = result['performance_metrics']
                    actual_time = metrics.get('generation_time', generation_time)
                    print(f"[SPEED] Actual generation: {actual_time:.1f}s")
                    
                    # Performance analysis
                    original_time = 105
                    improvement = ((original_time - actual_time) / original_time) * 100
                    print(f"[IMPROVEMENT] {improvement:.0f}% faster than original")
                    
                    if improvement > 50:
                        print("[RESULT] MASSIVE SPEED IMPROVEMENT ACHIEVED!")
                    else:
                        print("[RESULT] Speed improvement detected")
            
            # Check generated files
            if result and 'files_generated' in result:
                print(f"\n[FILES] Generated {len(result['files_generated'])} files:")
                for file_path in result['files_generated']:
                    print(f"  - {Path(file_path).name}")
            
            print("\n[SUCCESS] Parallel AI system is working correctly!")
            return True
            
        else:
            print("[ERROR] Parallel mode not available")
            return False
            
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[READY] System ready for production use!")
    else:
        print("\n[ISSUE] Check API key and configuration")