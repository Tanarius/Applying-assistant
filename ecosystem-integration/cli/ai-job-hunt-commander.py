#!/usr/bin/env python3
"""
AI Job Hunt Commander - Professional Job Application Automation
==============================================================

Enhanced job application system combining AI company research, resume customization,
and intelligent cover letter generation for Infrastructure to AI career transition.

Author: Trey (Infrastructure Engineer to AI/Automation Specialist)
Purpose: Automate complete job application process while showcasing AI engineering skills
Connection: Integrates with the automation ecosystem to provide comprehensive job search support.

Features:
- AI-powered company intelligence gathering using OpenAI
- Dynamic resume customization based on job requirements  
- Intelligent cover letter generation with company insights
- Complete application packaging and tracking
- Analytics and performance optimization

Usage:
    python ai-job-hunt-commander.py --company "TechCorp" --title "AI Engineer"
    python ai-job-hunt-commander.py --url "https://job-posting-url.com"
    python ai-job-hunt-commander.py --analytics
"""

import sys
import argparse
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

try:
    from main_application_engine import ApplicationEngine
except ImportError as e:
    print(f"Error importing AI Job Hunt Commander modules: {e}")
    print("Please ensure all required files are in the src directory.")
    sys.exit(1)

class AIJobHuntCommanderCLI:
    """
    Command line interface for AI Job Hunt Commander
    
    Provides professional interface matching the automation bot ecosystem style
    while delivering comprehensive job application automation capabilities.
    """
    
    def __init__(self):
        self.engine = ApplicationEngine(output_dir="Generated_Applications")
        self.display_header()
    
    def display_header(self):
        """Display professional header matching bot ecosystem style"""
        print("\n" + "="*80)
        print("AI JOB HUNT COMMANDER - Professional Application Automation")
        print("="*80)
        print("Infrastructure Engineer to AI/Automation Specialist | Career Transition Toolkit")
        print("Triple-Duty Strategy: Job Search + Skills Showcase + Portfolio Building")
        print("="*80)
    
    def run_interactive_mode(self):
        """Interactive mode for comprehensive job application generation"""
        print("\n* INTERACTIVE APPLICATION GENERATOR")
        print("-" * 50)
        
        print("Choose your input method:")
        print("1. Job Posting URL (automatic scraping)")
        print("2. Manual Company + Job Title Entry") 
        print("3. Pre-parsed Job Data (JSON)")
        print("4. View Analytics Dashboard")
        print("5. Exit")
        
        while True:
            try:
                choice = input("\nSelect option (1-5): ").strip()
                
                if choice == "1":
                    self.handle_url_input()
                elif choice == "2":
                    self.handle_manual_input()
                elif choice == "3":
                    self.handle_json_input()
                elif choice == "4":
                    self.show_analytics()
                elif choice == "5":
                    print("\n*** Thanks for using AI Job Hunt Commander! ***")
                    print("* Connect with other automation bots in the ecosystem")
                    break
                else:
                    print("X Invalid choice. Please select 1-5.")
                    
            except KeyboardInterrupt:
                print("\n\n*** Exiting AI Job Hunt Commander. Happy job hunting! ***")
                break
            except Exception as e:
                print(f"X Error: {e}")
    
    def handle_url_input(self):
        """Handle job posting URL input"""
        print("\n* JOB URL PROCESSING")
        print("-" * 30)
        
        url = input("Enter job posting URL: ").strip()
        if not url:
            print("X URL cannot be empty")
            return
            
        print(f"\n* Processing job posting from: {url}")
        print("⚠️  Note: Advanced web scraping coming in Layer 2")
        print("* For now, please use manual entry mode for best results")
    
    def handle_manual_input(self):
        """Handle manual company and job title input"""
        print("\n* MANUAL JOB APPLICATION GENERATION")
        print("-" * 40)
        
        company = input("Company Name: ").strip()
        if not company:
            print("X Company name cannot be empty")
            return
            
        job_title = input("Job Title: ").strip() 
        if not job_title:
            print("X Job title cannot be empty")
            return
        
        print(f"\n* Generating complete application package for:")
        print(f"   Company: {company}")
        print(f"   Position: {job_title}")
        print("\n" + "-" * 50)
        
        try:
            # Generate application package
            package = self.engine.process_job_application(
                company_name=company,
                job_title=job_title
            )
            
            if package:
                self.display_success_summary(package)
                self.offer_integration_options(package)
            else:
                print("X Application generation failed. Please try again.")
                
        except Exception as e:
            print(f"X Error generating application: {e}")
    
    def handle_json_input(self):
        """Handle pre-parsed JSON job data"""
        print("\n* JSON JOB DATA PROCESSING")
        print("-" * 35)
        print("* Feature coming in Layer 2 - Advanced data integration")
        print("* Will integrate with tailored-apply-bot JSON outputs")
    
    def show_analytics(self):
        """Display analytics dashboard"""
        print("\n* APPLICATION ANALYTICS DASHBOARD")
        print("-" * 40)
        
        try:
            analytics = self.engine.get_application_analytics()
            
            if analytics.get('total_applications', 0) == 0:
                print("* No applications generated yet.")
                print("* Generate your first application to see analytics!")
                return
            
            print(f"* Total Applications: {analytics['total_applications']}")
            print(f"* Average Score: {analytics['average_score']:.1f}/10")
            print(f"* Companies Applied: {analytics['companies_applied']}")
            
            # Score distribution
            dist = analytics['score_distribution']
            print(f"\n* Score Distribution:")
            print(f"   * High (8.0+): {dist['high']} applications")
            print(f"   * Medium (6.0-7.9): {dist['medium']} applications")
            print(f"   * Low (<6.0): {dist['low']} applications")
            
            # Recent applications
            if analytics['recent_applications']:
                print(f"\n* Recent Applications:")
                for app in analytics['recent_applications']:
                    print(f"   • {app['company']} - {app['title']} ({app['score']:.1f}/10) [{app['date']}]")
            
        except Exception as e:
            print(f"X Error loading analytics: {e}")
    
    def display_success_summary(self, package):
        """Display success summary with ecosystem integration hints"""
        print("\n*** APPLICATION PACKAGE COMPLETED! ***")
        print("="*60)
        
        print(f"* Application ID: {package['application_id']}")
        print(f"* Quality Score: {package['application_score']:.1f}/10")
        print(f"* Files Generated: {len(package['files_generated'])}")
        
        print(f"\n* Generated Files:")
        for file_path in package['files_generated']:
            print(f"   • {Path(file_path).name}")
        
        print(f"\n* Next Steps Preview:")
        for i, step in enumerate(package['next_steps'][:3], 1):
            print(f"   {i}. {step}")
    
    def offer_integration_options(self, package):
        """Offer integration with other automation bots"""
        print(f"\n* ECOSYSTEM INTEGRATION OPTIONS")
        print("-" * 40)
        print("1. Generate GitHub development log content")
        print("2. Create LinkedIn post about application process")
        print("3. Update portfolio with new automation showcase")
        print("4. Return to main menu")
        
        choice = input("\nSelect integration option (1-4): ").strip()
        
        if choice == "1":
            print("* Integration with GitHub Dev Logger Bot:")
            print(f"   Content: 'Automated job application for {package['job_information']['company']}'")
            print(f"   🏷️  Tags: #JobSearch #Automation #AI #CareerTransition")
            print("   * Run GitHub Dev Logger to generate full content!")
        
        elif choice == "2":
            print("* LinkedIn Post Suggestion:")
            print(f"   🎯 'Just automated my application to {package['job_information']['company']}'")
            print(f"   'AI Job Hunt Commander generated {package['application_score']:.1f}/10 quality package'")
            print("   'Infrastructure to AI transition in action!'")
        
        elif choice == "3":
            print("* Portfolio Update Ideas:")
            print("   'Add AI Job Hunt Commander to project showcase'")
            print("   🎨 'Update skills section with automation capabilities'")
            print("   'Display application success metrics'")
        
        print(f"\n* Returning to main menu...")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI Job Hunt Commander - Professional Application Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python ai-job-hunt-commander.py --company "OpenAI" --title "AI Engineer"
    python ai-job-hunt-commander.py --url "https://jobs.company.com/posting"
    python ai-job-hunt-commander.py --analytics
    python ai-job-hunt-commander.py  # Interactive mode
        """
    )
    
    parser.add_argument('--company', help='Target company name')
    parser.add_argument('--title', help='Job title/position')
    parser.add_argument('--url', help='Job posting URL')
    parser.add_argument('--analytics', action='store_true', help='Show analytics dashboard')
    parser.add_argument('--output-dir', default='Generated_Applications', help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = AIJobHuntCommanderCLI()
    
    # Handle command line arguments
    if args.analytics:
        cli.show_analytics()
    elif args.company and args.title:
        engine = ApplicationEngine(output_dir=args.output_dir)
        package = engine.process_job_application(
            company_name=args.company,
            job_title=args.title
        )
        if package:
            cli.display_success_summary(package)
    elif args.url:
        print(f"* URL processing: {args.url}")
        print("* Advanced web scraping coming in Layer 2")
        print("* Use --company and --title for immediate results")
    else:
        # Interactive mode
        cli.run_interactive_mode()

if __name__ == "__main__":
    main()