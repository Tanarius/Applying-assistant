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
from api_key_manager import find_openai_api_key, get_working_api_key
from ai_powered_application_engine import AIPoweredApplicationEngine
from parallel_ai_engine import ParallelAIEngine
import asyncio

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
        
        # Detect OpenAI API key
        self.api_key = openai_api_key or find_openai_api_key()
        
        # Determine operation mode
        if self.api_key:
            print("* OpenAI API key detected - ENABLING SOPHISTICATED PARALLEL AI MODE")
            print("* Maximum quality with GPT-4 + parallel processing (35-40 seconds)")
            print("* Sophisticated tailoring with advanced strategic positioning")
            self.parallel_ai_engine = ParallelAIEngine(openai_api_key=self.api_key)
            self.ai_mode = True
            self.parallel_mode = True
        else:
            print("* No OpenAI API key found - USING TEMPLATE MODE")
            print("* Instant generation with basic templates")
            # Initialize legacy components for template mode
            self.company_researcher = AICompanyResearcher(None)
            self.resume_engine = EnhancedResumeEngine(None)
            self.cover_letter_generator = IntelligentCoverLetterGenerator(None)
            self.ai_mode = False
            self.parallel_mode = False
        
        # Application tracking
        self.applications = {}
        self.load_application_history()
        
        mode_text = "AI-POWERED" if self.ai_mode else "TEMPLATE"
        print(f"AI Job Hunt Commander ready - {mode_text} MODE")
    
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
        
        # Route to appropriate engine based on API key availability
        if self.ai_mode and self.parallel_mode:
            return self._process_with_parallel_ai_engine(job_data)
        elif self.ai_mode:
            return self._process_with_ai_engine(job_data)
        else:
            return self._process_with_template_mode(job_data)
    
    def _process_with_parallel_ai_engine(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process application using sophisticated parallel AI engine"""
        print("\n* USING SOPHISTICATED PARALLEL AI MODE - Maximum quality + speed")
        print("* GPT-4 for all tasks + parallel processing (35-40 seconds)")
        print("* Advanced strategic positioning and technical depth")
        
        # Run parallel AI engine asynchronously
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            parallel_application = loop.run_until_complete(
                self.parallel_ai_engine.generate_sophisticated_application(
                    job_title=job_data.get('title', ''),
                    company_name=job_data.get('company', ''),
                    job_description=job_data.get('description', ''),
                    job_url=job_data.get('url', '')
                )
            )
            
            # Create package compatible with existing interface
            application_package = {
                'application_id': self._generate_application_id(job_data),
                'generated_at': datetime.now().isoformat(),
                'job_information': job_data,
                'parallel_ai_application': parallel_application.__dict__,
                'application_score': parallel_application.sophistication_score,
                'files_generated': [],
                'mode': 'SOPHISTICATED_PARALLEL_AI',
                'next_steps': self._generate_sophisticated_next_steps(parallel_application),
                'performance_metrics': {
                    'generation_time': parallel_application.generation_time,
                    'sophistication_score': parallel_application.sophistication_score,
                    'personalization_depth': parallel_application.personalization_depth,
                    'strategic_insight_score': parallel_application.strategic_insight_score,
                    'parallel_efficiency': parallel_application.parallel_efficiency,
                    'api_calls_made': parallel_application.api_calls_made
                }
            }
            
            # Save sophisticated application to file
            app_dir = self.output_dir / application_package['application_id']
            app_dir.mkdir(exist_ok=True)
            
            sophisticated_file = self._save_sophisticated_application(parallel_application, app_dir)
            application_package['files_generated'].append(sophisticated_file)
            
            # Save tracking data
            self._save_application(application_package)
            self._print_sophisticated_application_summary(application_package)
            
            return application_package
            
        except Exception as e:
            print(f"❌ Parallel AI processing failed: {e}")
            print("🔄 Falling back to standard AI mode...")
            return self._process_with_ai_engine(job_data)
    
    def _process_with_ai_engine(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process application using AI-powered engine"""
        print("\n* USING AI-POWERED MODE - Deep research in progress...")
        print("* This will take 60-120 seconds for comprehensive analysis")
        
        # Use the AI engine for comprehensive generation
        ai_application = self.ai_engine.generate_ai_application(
            job_title=job_data.get('title', ''),
            company_name=job_data.get('company', ''),
            job_description=job_data.get('description', ''),
            job_url=job_data.get('url', '')
        )
        
        # Create package compatible with existing interface
        application_package = {
            'application_id': self._generate_application_id(job_data),
            'generated_at': datetime.now().isoformat(),
            'job_information': job_data,
            'ai_application': ai_application.__dict__,
            'application_score': ai_application.ai_quality_score,
            'files_generated': [],
            'mode': 'AI_POWERED',
            'next_steps': self._generate_ai_next_steps(ai_application)
        }
        
        # Save AI application to file
        app_dir = self.output_dir / application_package['application_id']
        app_dir.mkdir(exist_ok=True)
        
        ai_file = self.ai_engine.save_ai_application(ai_application, app_dir)
        application_package['files_generated'].append(ai_file)
        
        # Save tracking data
        self._save_application(application_package)
        self._print_ai_application_summary(application_package)
        
        return application_package
    
    def _process_with_template_mode(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process application using template mode (legacy)"""
        print("\n* USING TEMPLATE MODE - Instant generation")
        
        # Step 2: AI Company Research
        print("\n* Phase 1: Basic Company Intelligence Gathering")
        company_intelligence = self.company_researcher.research_company(
            job_data.get('company', 'Unknown'),
            job_data.get('title')
        )
        
        # Step 3: AI Resume Customization
        print("\n* Phase 2: Resume Template Customization")
        resume_customization = self.resume_engine.customize_resume_for_job(
            job_data,
            company_intelligence.__dict__ if company_intelligence else None
        )
        
        # Step 4: Intelligent Cover Letter Generation
        print("\n* Phase 3: Cover Letter Template Generation")
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
    
    def _generate_ai_next_steps(self, ai_application) -> List[str]:
        """Generate next steps for AI-powered applications"""
        return [
            "Review comprehensive AI-generated application package",
            "Customize cover letter with personal touches if needed",
            "Submit through company's preferred application channel",
            "Follow strategic positioning recommendations from research",
            "Prepare for interview using AI-generated preparation guide",
            "Schedule follow-up based on success strategy recommendations"
        ]
    
    def _print_ai_application_summary(self, package: Dict[str, Any]) -> None:
        """Print summary for AI-powered applications"""
        print("\n" + "="*80)
        print("*** AI-POWERED JOB APPLICATION COMPLETED ***")
        print("="*80)
        
        # Basic info
        job_info = package['job_information']
        ai_app = package['ai_application']
        
        print(f"* Position: {job_info.get('title', 'Unknown')}")
        print(f"* Company: {job_info.get('company', 'Unknown')}")
        print(f"* Application ID: {package['application_id']}")
        print(f"* Generation Mode: AI-POWERED (Deep Research)")
        print(f"* Time Invested: {ai_app.get('time_invested', 0):.1f} seconds")
        
        # Quality metrics
        print(f"\n* QUALITY SCORES:")
        print(f"   Research Depth: {ai_app.get('research_depth_score', 0):.1f}/10")
        print(f"   AI Content Quality: {ai_app.get('ai_quality_score', 0):.1f}/10")
        print(f"   Personalization: {ai_app.get('personalization_score', 0):.1f}/10")
        
        # Strategic insights
        print(f"\n* STRATEGIC POSITIONING:")
        positioning = ai_app.get('strategic_positioning', 'N/A')[:100]
        print(f"   {positioning}...")
        
        # Files generated
        print(f"\n* FILES GENERATED:")
        for file_path in package['files_generated']:
            print(f"   - {file_path}")
        
        # Next steps
        print(f"\n* RECOMMENDED NEXT STEPS:")
        for i, step in enumerate(package['next_steps'][:4], 1):
            print(f"   {i}. {step}")
        
        print("\n" + "="*80)
        print("*** HIGH-QUALITY AI APPLICATION READY FOR SUBMISSION! ***")
        print("="*80)
    
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
    
    def _generate_sophisticated_next_steps(self, parallel_application) -> List[str]:
        """Generate sophisticated next steps for parallel AI applications"""
        return [
            "Review comprehensive sophisticated AI-generated application package",
            "Leverage advanced strategic positioning and competitive analysis",
            "Utilize sophisticated interview preparation and technical depth guide",
            "Implement executive-level success strategy and differentiation approach",
            "Follow advanced career narrative and technical leadership positioning",
            "Execute strategic application timeline with sophisticated follow-up approach"
        ]
    
    def _save_sophisticated_application(self, parallel_application, app_dir) -> str:
        """Save sophisticated parallel application to file"""
        filename = f"Sophisticated_Parallel_{parallel_application.company_name}_{parallel_application.job_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = app_dir / filename
        
        content = f"""================================================================================
  SOPHISTICATED PARALLEL AI APPLICATION PACKAGE
================================================================================

APPLICATION OVERVIEW
Job Title: {parallel_application.job_title}
Company: {parallel_application.company_name}
Application Date: {parallel_application.application_date}

PERFORMANCE METRICS
Generation Time: {parallel_application.generation_time:.1f} seconds
Sophistication Score: {parallel_application.sophistication_score}/10
Personalization Depth: {parallel_application.personalization_depth}/10
Strategic Insight Score: {parallel_application.strategic_insight_score}/10
Parallel Efficiency: {parallel_application.parallel_efficiency:.1%}
API Calls Made: {parallel_application.api_calls_made}
Optimization Level: {parallel_application.optimization_level}

================================================================================
  EXECUTIVE SUMMARY
================================================================================

{parallel_application.executive_summary}

================================================================================
  SOPHISTICATED COVER LETTER
================================================================================

{parallel_application.cover_letter}

================================================================================
  STRATEGIC POSITIONING & COMPETITIVE ADVANTAGE
================================================================================

{parallel_application.strategic_positioning}

================================================================================
  ADVANCED COMPANY INTELLIGENCE
================================================================================

{parallel_application.company_intelligence}

================================================================================
  COMPETITIVE ANALYSIS
================================================================================

{parallel_application.competitive_analysis}

================================================================================
  TECHNICAL ALIGNMENT & REQUIREMENTS
================================================================================

{parallel_application.technical_alignment}

================================================================================
  SOPHISTICATED INTERVIEW PREPARATION
================================================================================

{parallel_application.interview_preparation}

================================================================================
  STRATEGIC SUCCESS PLAN
================================================================================

{parallel_application.success_strategy}

================================================================================
  CAREER TRANSITION NARRATIVE
================================================================================

{parallel_application.career_narrative}

================================================================================
  GENERATION DETAILS
================================================================================

Generated by: Sophisticated Parallel AI Engine
Model Used: GPT-4 (maximum quality)
Processing Method: Parallel execution with sophisticated prompting
Quality Assurance: Multi-layer strategic analysis and technical depth
Optimization: Maximum sophistication with speed enhancement

Infrastructure Engineer to AI/ML Leadership Career Transition
Executive-Level Sophisticated Application Package

================================================================================
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def _print_sophisticated_application_summary(self, package: Dict[str, Any]) -> None:
        """Print summary for sophisticated parallel applications"""
        print("\n" + "="*80)
        print("*** SOPHISTICATED PARALLEL AI APPLICATION COMPLETED ***")
        print("="*80)
        
        # Basic info
        job_info = package['job_information']
        metrics = package['performance_metrics']
        
        print(f"* Position: {job_info.get('title', 'Unknown')}")
        print(f"* Company: {job_info.get('company', 'Unknown')}")
        print(f"* Application ID: {package['application_id']}")
        print(f"* Generation Mode: SOPHISTICATED PARALLEL AI")
        print(f"* Processing Time: {metrics.get('generation_time', 0):.1f} seconds")
        
        # Quality metrics
        print(f"\n* SOPHISTICATION METRICS:")
        print(f"   Overall Quality: {metrics.get('sophistication_score', 0):.1f}/10")
        print(f"   Personalization Depth: {metrics.get('personalization_depth', 0):.1f}/10")
        print(f"   Strategic Insight: {metrics.get('strategic_insight_score', 0):.1f}/10")
        print(f"   Parallel Efficiency: {metrics.get('parallel_efficiency', 0):.1%}")
        print(f"   API Calls Optimized: {metrics.get('api_calls_made', 0)}")
        
        # Performance comparison
        original_time = 105  # seconds
        current_time = metrics.get('generation_time', 0)
        time_saved = original_time - current_time
        speed_improvement = (time_saved / original_time) * 100
        
        print(f"\n* PERFORMANCE IMPROVEMENT:")
        print(f"   Time Saved: {time_saved:.1f} seconds")
        print(f"   Speed Improvement: {speed_improvement:.0f}% faster")
        print(f"   Quality Level: Executive/Sophisticated")
        
        # Files generated
        print(f"\n* FILES GENERATED:")
        for file_path in package['files_generated']:
            print(f"   - {Path(file_path).name}")
        
        # Next steps
        print(f"\n* SOPHISTICATED NEXT STEPS:")
        for i, step in enumerate(package['next_steps'][:4], 1):
            print(f"   {i}. {step}")
        
        print("\n" + "="*80)
        print("*** EXECUTIVE-LEVEL SOPHISTICATED APPLICATION READY! ***")
        print("="*80)

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