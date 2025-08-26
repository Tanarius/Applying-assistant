#!/usr/bin/env python3
"""
Main Application Engine
======================

Orchestrates the complete AI-powered job application process by integrating:
- Company intelligence gathering
- AI-powered resume customization  
- Intelligent cover letter generation
- Application tracking and analytics

This is the main entry point for the AI Job Hunt Commander system.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import our custom modules
from ai_company_research import AICompanyResearcher, CompanyIntelligence
from enhanced_resume_engine import EnhancedResumeEngine, ResumeCustomization
from intelligent_cover_letter import IntelligentCoverLetterGenerator, CoverLetterGeneration

class ApplicationEngine:
    """
    Main orchestration engine for AI-powered job applications
    
    Coordinates the entire process:
    1. Company research and intelligence gathering
    2. Resume customization based on job requirements
    3. Intelligent cover letter generation
    4. Application packaging and tracking
    5. Performance analytics and optimization
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, output_dir: str = "applications"):
        """Initialize the application engine with all components"""
        print("Initializing AI Job Hunt Commander Application Engine")
        
        # Set up output directory
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize AI components
        self.company_researcher = AICompanyResearcher(openai_api_key)
        self.resume_engine = EnhancedResumeEngine(openai_api_key)
        self.cover_letter_generator = IntelligentCoverLetterGenerator(openai_api_key)
        
        # Application tracking
        self.applications = {}
        self.load_application_history()
        
        print("AI Job Hunt Commander ready for intelligent job applications")
    
    def process_job_application(
        self, 
        job_url: Optional[str] = None,
        job_data: Optional[Dict[str, Any]] = None,
        company_name: Optional[str] = None,
        job_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete AI-powered job application processing
        
        Args:
            job_url: Optional job posting URL for scraping
            job_data: Pre-parsed job information
            company_name: Manual company name input
            job_title: Manual job title input
            
        Returns:
            Complete application package with all generated content
        """
        print("Starting AI-powered job application processing")
        
        # Step 1: Gather or parse job information
        if job_data:
            print("* Using provided job data")
        elif job_url:
            print(f"* Scraping job posting from: {job_url}")
            job_data = self._scrape_job_posting(job_url)
        elif company_name and job_title:
            print(f"* Creating job data for {job_title} at {company_name}")
            job_data = {
                'title': job_title,
                'company': company_name,
                'description': f"Manually entered position: {job_title} at {company_name}",
                'url': None
            }
        else:
            raise ValueError("Must provide either job_url, job_data, or company_name + job_title")
        
        if not job_data:
            print("X Failed to gather job information")
            return None
        
        print(f"* Processing: {job_data.get('title', 'Unknown Role')} at {job_data.get('company', 'Unknown Company')}")
        
        # Step 2: AI Company Research
        print("\n* Phase 1: AI Company Intelligence Gathering")
        company_intelligence = self.company_researcher.research_company(
            job_data.get('company', 'Unknown'),
            job_data.get('title')
        )
        
        # Step 3: AI Resume Customization
        print("\n* Phase 2: AI-Powered Resume Customization")
        resume_customization = self.resume_engine.customize_resume_for_job(
            job_data,
            company_intelligence.__dict__ if company_intelligence else None
        )
        
        # Step 4: Intelligent Cover Letter Generation
        print("\n* Phase 3: Intelligent Cover Letter Generation")
        cover_letter = self.cover_letter_generator.generate_cover_letter(
            job_data,
            company_intelligence
        )
        
        # Step 5: Package and Export Application
        print("\n* Phase 4: Application Packaging & Export")
        application_package = self._create_application_package(
            job_data,
            company_intelligence,
            resume_customization,
            cover_letter
        )
        
        # Step 6: Save and Track
        print("\n* Phase 5: Application Tracking & Analytics")
        self._save_application(application_package)
        
        # Step 7: Generate Summary Report
        self._print_application_summary(application_package)
        
        return application_package
    
    def _scrape_job_posting(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape job posting from URL (enhanced version of existing scraper)"""
        # This would integrate with the existing tailored-apply-bot scraping logic
        # For now, return mock data for testing
        print("! Job scraping not yet implemented - using manual input mode")
        return None
    
    def _create_application_package(
        self,
        job_data: Dict[str, Any],
        company_intel: CompanyIntelligence,
        resume_custom: ResumeCustomization,
        cover_letter: CoverLetterGeneration
    ) -> Dict[str, Any]:
        """Create comprehensive application package with all components"""
        
        # Generate unique application ID
        app_id = self._generate_application_id(job_data)
        
        # Create package structure
        package = {
            'application_id': app_id,
            'generated_at': datetime.now().isoformat(),
            'job_information': job_data,
            'company_intelligence': company_intel.__dict__ if company_intel else {},
            'resume_customization': resume_custom.__dict__ if resume_custom else {},
            'cover_letter': cover_letter.__dict__ if cover_letter else {},
            'files_generated': [],
            'application_score': self._calculate_application_score(company_intel, resume_custom, cover_letter),
            'next_steps': self._generate_next_steps(job_data, company_intel)
        }
        
        # Export files to application directory
        app_dir = self.output_dir / app_id
        app_dir.mkdir(exist_ok=True)
        
        # Export resume
        if resume_custom:
            resume_file = self.resume_engine.export_resume_markdown(
                resume_custom, 
                str(app_dir / f"resume_{app_id}.md")
            )
            package['files_generated'].append(resume_file)
        
        # Export cover letter
        if cover_letter:
            cover_letter_file = self.cover_letter_generator.export_cover_letter(
                cover_letter,
                str(app_dir / f"cover_letter_{app_id}.txt")
            )
            package['files_generated'].append(cover_letter_file)
        
        # Export company research
        if company_intel:
            research_file = self.company_researcher.export_research(
                company_intel,
                str(app_dir / f"company_research_{app_id}.json")
            )
            package['files_generated'].append(research_file)
        
        # Export application summary
        summary_file = str(app_dir / f"application_summary_{app_id}.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2, ensure_ascii=False, default=str)
        package['files_generated'].append(summary_file)
        
        return package
    
    def _generate_application_id(self, job_data: Dict[str, Any]) -> str:
        """Generate unique application identifier"""
        company = job_data.get('company', 'unknown').replace(' ', '_').replace('-', '_')
        company = ''.join(c for c in company if c.isalnum() or c == '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"{company}_{timestamp}"
    
    def _calculate_application_score(
        self,
        company_intel: Optional[CompanyIntelligence],
        resume_custom: Optional[ResumeCustomization],
        cover_letter: Optional[CoverLetterGeneration]
    ) -> float:
        """Calculate overall application quality score (0-10)"""
        score = 5.0  # Base score
        
        # Company research quality
        if company_intel:
            if company_intel.job_fit_score:
                score += (company_intel.job_fit_score - 5.0) * 0.3
            if len(company_intel.recent_news) > 0:
                score += 0.5
            if len(company_intel.application_recommendations) > 3:
                score += 0.5
        
        # Resume customization quality
        if resume_custom:
            if len(resume_custom.emphasized_skills) >= 5:
                score += 0.5
            if len(resume_custom.keyword_optimization) >= 5:
                score += 0.5
        
        # Cover letter personalization
        if cover_letter:
            score += (cover_letter.personalization_score - 5.0) * 0.2
        
        return min(max(score, 0.0), 10.0)
    
    def _generate_next_steps(
        self, 
        job_data: Dict[str, Any], 
        company_intel: Optional[CompanyIntelligence]
    ) -> List[str]:
        """Generate recommended next steps for this application"""
        steps = []
        
        # Basic application steps
        steps.append("Review and customize generated resume for final submission")
        steps.append("Personalize cover letter opening with specific company details")
        steps.append("Submit application through company's preferred channel")
        
        # Company-specific steps
        if company_intel and company_intel.application_recommendations:
            steps.extend([
                f"Application tip: {rec}" for rec in company_intel.application_recommendations[:2]
            ])
        
        # Follow-up planning
        steps.append("Schedule follow-up reminder for 1 week after application")
        steps.append("Research hiring manager on LinkedIn for potential connection")
        
        return steps
    
    def _save_application(self, package: Dict[str, Any]) -> None:
        """Save application to tracking system"""
        app_id = package['application_id']
        self.applications[app_id] = package
        
        # Save to persistent storage
        tracking_file = self.output_dir / "application_tracking.json"
        with open(tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.applications, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"* Application saved and tracked: {app_id}")
    
    def load_application_history(self) -> None:
        """Load previous application history"""
        tracking_file = self.output_dir / "application_tracking.json"
        if tracking_file.exists():
            try:
                with open(tracking_file, 'r', encoding='utf-8') as f:
                    self.applications = json.load(f)
                print(f"* Loaded {len(self.applications)} previous applications")
            except Exception as e:
                print(f"! Could not load application history: {e}")
                self.applications = {}
        else:
            self.applications = {}
    
    def _print_application_summary(self, package: Dict[str, Any]) -> None:
        """Print comprehensive application summary"""
        print("\n" + "="*80)
        print("*** AI JOB APPLICATION COMPLETED ***")
        print("="*80)
        
        # Basic info
        job_info = package['job_information']
        print(f"* Position: {job_info.get('title', 'Unknown')}")
        print(f"* Company: {job_info.get('company', 'Unknown')}")
        print(f"* Application ID: {package['application_id']}")
        print(f"* Application Score: {package['application_score']:.1f}/10")
        
        # Company insights
        if package['company_intelligence']:
            intel = package['company_intelligence']
            print(f"\n* Company Intelligence:")
            print(f"   Industry: {intel.get('industry', 'N/A')}")
            print(f"   Job Fit Score: {intel.get('job_fit_score', 'N/A')}/10")
            if intel.get('recent_news'):
                print(f"   Latest News: {intel['recent_news'][0]}")
        
        # Resume customization
        if package['resume_customization']:
            resume = package['resume_customization']
            print(f"\n* Resume Customization:")
            print(f"   Template: {resume.get('version_name', 'N/A')}")
            if resume.get('emphasized_skills'):
                print(f"   Key Skills: {', '.join(resume['emphasized_skills'][:3])}")
        
        # Cover letter
        if package['cover_letter']:
            letter = package['cover_letter']
            print(f"\n* Cover Letter:")
            print(f"   Template: {letter.get('template_used', 'N/A')}")
            print(f"   Personalization: {letter.get('personalization_score', 0):.1f}/10")
        
        # Files generated
        print(f"\n* Files Generated:")
        for file_path in package['files_generated']:
            print(f"   - {file_path}")
        
        # Next steps
        print(f"\n* Recommended Next Steps:")
        for i, step in enumerate(package['next_steps'][:5], 1):
            print(f"   {i}. {step}")
        
        print("\n" + "="*80)
        print("*** Ready for submission! Review files and customize as needed. ***")
        print("="*80)
    
    def get_application_analytics(self) -> Dict[str, Any]:
        """Generate analytics across all applications"""
        if not self.applications:
            return {"message": "No applications found"}
        
        apps = list(self.applications.values())
        
        analytics = {
            'total_applications': len(apps),
            'average_score': sum(app.get('application_score', 0) for app in apps) / len(apps),
            'companies_applied': len(set(app['job_information'].get('company', 'Unknown') for app in apps)),
            'top_companies': {},
            'score_distribution': {'high': 0, 'medium': 0, 'low': 0},
            'recent_applications': []
        }
        
        # Score distribution
        for app in apps:
            score = app.get('application_score', 0)
            if score >= 8.0:
                analytics['score_distribution']['high'] += 1
            elif score >= 6.0:
                analytics['score_distribution']['medium'] += 1
            else:
                analytics['score_distribution']['low'] += 1
        
        # Top companies
        for app in apps:
            company = app['job_information'].get('company', 'Unknown')
            analytics['top_companies'][company] = analytics['top_companies'].get(company, 0) + 1
        
        # Recent applications (last 5)
        sorted_apps = sorted(apps, key=lambda x: x.get('generated_at', ''), reverse=True)
        analytics['recent_applications'] = [
            {
                'company': app['job_information'].get('company'),
                'title': app['job_information'].get('title'),
                'score': app.get('application_score'),
                'date': app.get('generated_at', '')[:10]
            }
            for app in sorted_apps[:5]
        ]
        
        return analytics

def main():
    """Command line interface for the Application Engine"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Job Hunt Commander - Intelligent Application Generation')
    parser.add_argument('--company', required=True, help='Target company name')
    parser.add_argument('--title', required=True, help='Job title')
    parser.add_argument('--url', help='Job posting URL (optional)')
    parser.add_argument('--output-dir', default='applications', help='Output directory for generated files')
    
    args = parser.parse_args()
    
    print("AI Job Hunt Commander - Application Engine")
    print("="*60)
    
    # Initialize engine
    engine = ApplicationEngine(output_dir=args.output_dir)
    
    # Process application
    try:
        package = engine.process_job_application(
            job_url=args.url,
            company_name=args.company,
            job_title=args.title
        )
        
        if package:
            print(f"\n*** SUCCESS! Application package created: {package['application_id']} ***")
        else:
            print("\nX Application processing failed")
            
    except Exception as e:
        print(f"\nX Error processing application: {e}")
        sys.exit(1)

def test_application_engine():
    """Test the complete application engine"""
    print("Testing Complete AI Application Engine")
    
    # Initialize engine
    engine = ApplicationEngine(output_dir="test_applications")
    
    # Test application
    test_package = engine.process_job_application(
        company_name="TechCorp AI",
        job_title="AI Engineer"
    )
    
    if test_package:
        print("\n*** Application engine test completed successfully! ***")
        
        # Show analytics
        analytics = engine.get_application_analytics()
        print(f"\n* Analytics: {analytics['total_applications']} applications with avg score {analytics['average_score']:.1f}")
    else:
        print("\nX Application engine test failed")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Run test if no arguments provided
        test_application_engine()
    else:
        # Run CLI interface
        main()