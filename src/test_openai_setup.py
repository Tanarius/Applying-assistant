#!/usr/bin/env python3
"""
OpenAI Setup Test
================

Quick test to verify your OpenAI API key is working
and demonstrate the difference between template and AI mode.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import os
import sys
import time
from pathlib import Path

def test_openai_setup():
    """Test OpenAI API key setup"""
    print("\n" + "="*80)
    print("OPENAI API SETUP TEST")
    print("="*80)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("X No OpenAI API key found")
        print("\n* SETUP REQUIRED:")
        print("1. Get API key from: https://platform.openai.com/api-keys")
        print("2. Set environment variable:")
        print("   Windows: setx OPENAI_API_KEY \"your-key-here\"")
        print("3. Restart terminal and try again")
        print("\n* See SETUP_OPENAI_API.md for detailed instructions")
        return False
    
    print(f"+ API key found: {api_key[:10]}...")
    
    # Test OpenAI import and client
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        print("+ OpenAI client initialized successfully")
    except ImportError:
        print("X OpenAI package not installed")
        print("* Run: pip install openai")
        return False
    except Exception as e:
        print(f"X OpenAI client error: {e}")
        return False
    
    # Test API call
    print("\n* Testing API connection...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "Say 'API test successful' if you can read this."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"+ API test successful: {result}")
        
    except Exception as e:
        print(f"X API test failed: {e}")
        print("* Check your API key and account credits")
        return False
    
    print("\n" + "="*80)
    print("* OPENAI SETUP COMPLETE - READY FOR AI APPLICATIONS!")
    print("="*80)
    return True

def demonstrate_quality_difference():
    """Show the difference between template and AI mode"""
    print("\n" + "="*80)
    print("QUALITY COMPARISON DEMO")
    print("="*80)
    
    print("* TEMPLATE MODE (Instant, Mediocre):")
    print("-" * 50)
    print("""
    Dear OpenAI Hiring Team,
    
    I am writing to express my interest in the Senior Infrastructure Engineer position.
    As an Infrastructure Engineer with 5+ years experience, I bring proven skills
    in system reliability and automation.
    
    [Generic template content continues...]
    """)
    
    print("\n* AI MODE (60+ seconds, High Quality):")  
    print("-" * 50)
    print("""
    Dear OpenAI Hiring Team,
    
    I am writing to express my strong interest in the Senior Infrastructure Engineer - 
    AI Platform position at OpenAI. Having researched your recent infrastructure 
    scaling challenges around ChatGPT's 100M+ weekly users and the technical 
    complexity of managing 25,000+ GPU training clusters, I'm excited to bring my 
    99.8% uptime track record to your AI model serving infrastructure.
    
    Your company's explosive growth from research lab to $1B+ revenue platform 
    creates unique infrastructure challenges that align perfectly with my experience 
    in production system reliability. My background scaling Python automation 
    systems and managing high-availability infrastructure directly addresses OpenAI's 
    core challenge: maintaining 99.9% uptime for real-time AI inference at 
    unprecedented scale.
    
    [Continues with specific company insights, technical understanding, 
     and strategic career positioning...]
    """)
    
    print("\n* QUALITY COMPARISON:")
    print("Template Mode: Generic, could apply to any company")
    print("AI Mode: Company-specific research, strategic positioning, technical depth")
    print("\n* TIME INVESTMENT:")
    print("Template Mode: 0 seconds (instant)")  
    print("AI Mode: 60-120 seconds (deep research + generation)")
    print("\n* COST:")
    print("Template Mode: Free")
    print("AI Mode: ~$0.50-2.00 per application")
    print("\n* RESULTS:")
    print("Template Mode: Low response rate, generic positioning")
    print("AI Mode: Higher response rate, strategic differentiation")

def main():
    """Main test function"""
    print("* Testing OpenAI API Setup...")
    
    if test_openai_setup():
        demonstrate_quality_difference()
        
        print(f"\n* READY TO GENERATE AI-POWERED APPLICATIONS!")
        print("Run: python ai_powered_application_engine.py")
        print("Expected time: 60-120 seconds for deep AI analysis")
        
        return True
    else:
        print(f"\nX Setup incomplete. See SETUP_OPENAI_API.md for help.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)