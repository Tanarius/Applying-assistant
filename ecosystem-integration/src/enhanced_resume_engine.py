#!/usr/bin/env python3
"""
Enhanced Resume Engine
=====================

AI-powered resume customization that adapts your Infrastructure to AI transition
resume based on specific job requirements and company research.

Features:
- Dynamic skill emphasis based on job requirements
- ATS optimization for keyword matching
- Company culture adaptation
- Achievement quantification
- Multiple format generation (PDF, Word, plain text)
- A/B testing version management
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# Optional OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

@dataclass
class ResumeProfile:
    """Your professional profile data"""
    name: str
    current_role: str
    target_role: str
    email: str
    phone: str
    location: str
    portfolio_url: str
    github_url: str
    linkedin_url: str
    
    # Experience sections
    professional_summary: str
    key_achievements: List[str]
    technical_skills: Dict[str, List[str]]
    work_experience: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[Dict[str, str]]

@dataclass  
class ResumeCustomization:
    """Customization instructions for specific job"""
    job_title: str
    company_name: str
    emphasized_skills: List[str]
    highlighted_achievements: List[str]
    customized_summary: str
    keyword_optimization: List[str]
    culture_adaptations: List[str]
    version_name: str

class EnhancedResumeEngine:
    """
    AI-powered resume customization engine
    
    Takes your base resume and adapts it for specific jobs using:
    - Job requirement analysis
    - Company culture research  
    - ATS keyword optimization
    - Achievement quantification
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize with OpenAI API key and load base resume"""
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if self.openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_api_key
        
        # Load your base professional profile
        self.base_profile = self._load_base_profile()
        
        # Resume version tracking
        self.resume_versions = {}
        
    def _load_base_profile(self) -> ResumeProfile:
        """Load your base professional profile"""
        return ResumeProfile(
            name="Treyten Ellingson",
            current_role="Infrastructure Engineer",
            target_role="AI/Automation Engineer",
            email="treyten@yahoo.com",
            phone="817-229-2040",
            location="Pflugerville, TX",
            portfolio_url="https://tanarius.github.io",
            github_url="https://github.com/Tanarius",
            linkedin_url="www.linkedin.com",
            
            professional_summary="""Infrastructure Engineer transitioning to AI/Automation with 4+ years of proven experience optimizing IT environments and managing Active Directory systems with >99.8% uptime. Currently building Python automation and data processing systems, including production-ready GitHub API integration and automated content generation. Combines deep infrastructure reliability knowledge with emerging AI/automation skills through systematic hands-on learning. Seeking AI/Automation roles where infrastructure expertise accelerates intelligent system development and deployment.""",
            
            key_achievements=[
                "Maintained >99.8% uptime for 200+ user Active Directory environment over 1+ years",
                "Reduced manual operational workload by 40% through custom Python automation scripts",
                "Built production-ready GitHub Development Logger Bot with intelligent content generation",
                "Enhanced threat detection capabilities through advanced security monitoring implementation"
            ],
            
            technical_skills={
                "Programming & Automation": [
                    "Python Development & Automation",
                    "GitHub API Integration", 
                    "Automated Systems",
                    "Algorithm Development",
                    "Production Applications"
                ],
                "Infrastructure & Systems": [
                    "Microsoft Entra ID (Azure AD)",
                    "Microsoft Azure",
                    "Windows Server",
                    "Active Directory",
                    "DNS/DHCP Configuration"
                ],
                "Security & Monitoring": [
                    "Splunk",
                    "SolarWinds", 
                    "Vulnerability Assessment",
                    "Network Monitoring",
                    "System Security"
                ],
                "DevOps & Integration": [
                    "API Development",
                    "CI/CD Pipeline Understanding",
                    "Repository Management",
                    "Automated Documentation"
                ]
            },
            
            work_experience=[
                {
                    "title": "Infrastructure Engineer",
                    "company": "RIATA Technologies",
                    "location": "Austin, Texas Metropolitan Area",
                    "duration": "March 2024 - Present",
                    "achievements": [
                        "Manage Windows Server, Active Directory for 200+ users, maintaining >99.8% uptime through systematic monitoring and optimization",
                        "Enhance security posture using Splunk, SolarWinds; implement advanced threat detection and response protocols",
                        "Develop Python automation scripts reducing manual operational workload by 40%",
                        "Lead firewall reviews, patch management, and vulnerability assessments ensuring compliance and security",
                        "Architect backup and recovery solutions ensuring 100% data integrity and rapid recovery capabilities",
                        "Currently pursuing: AI/Automation transition through hands-on Python development and automation projects"
                    ]
                },
                {
                    "title": "System Administrator", 
                    "company": "Wolff Logics",
                    "location": "Austin, Texas Metropolitan Area",
                    "duration": "December 2022 - March 2024",
                    "achievements": [
                        "Managed user support and technical issue resolution, enhancing system reliability and performance",
                        "Configured and maintained systems ensuring optimal performance and minimal downtime",
                        "Collaborated on IT projects contributing to successful system upgrades and migrations",
                        "Implemented regular backup procedures safeguarding data and ensuring business continuity"
                    ]
                }
            ],
            
            projects=[
                {
                    "name": "GitHub Development Logger Bot",
                    "description": "Automated Content Generation System",
                    "date": "August 2025",
                    "url": "https://github.com/Tanarius/github-dev-logger-bot",
                    "details": [
                        "Built production-ready Python automation analyzing GitHub activity and generating professional content for LinkedIn, Twitter, and portfolio updates",
                        "Implemented intelligent commit filtering, technology detection, and multi-platform content optimization",
                        "Designed system serving portfolio demonstration, job search content, and personal brand building"
                    ],
                    "technologies": ["Python", "GitHub API", "automated workflows", "content generation algorithms"]
                },
                {
                    "name": "Personal Portfolio & Professional Website",
                    "description": "Responsive Web Application",
                    "date": "August 2025", 
                    "url": "https://tanarius.github.io",
                    "details": [
                        "Developed professional portfolio showcasing infrastructure-to-AI/automation transition journey",
                        "Implemented automated content integration and responsive design",
                        "Demonstrates technical skills through live project examples and documentation"
                    ],
                    "technologies": ["Web Development", "Responsive Design", "Automated Integration"]
                }
            ],
            
            education=[
                {
                    "degree": "Bachelor of Technology",
                    "institution": "University of Phoenix-Texas",
                    "duration": "December 2017 - December 2021"
                }
            ],
            
            certifications=[
                {
                    "name": "CompTIA Cybersecurity Analyst (CySA+)",
                    "issuer": "CompTIA",
                    "date": "January 2024"
                },
                {
                    "name": "Google Cybersecurity Certification", 
                    "issuer": "Coursera",
                    "date": "January 2024"
                }
            ]
        )
    
    def customize_resume_for_job(
        self, 
        job_data: Dict[str, Any], 
        company_intelligence: Optional[Dict] = None
    ) -> ResumeCustomization:
        """
        Create customized resume version for specific job
        
        Args:
            job_data: Job posting information
            company_intelligence: Optional company research data
            
        Returns:
            ResumeCustomization: Tailored resume configuration
        """
        print(f"* Customizing resume for {job_data.get('title', 'Unknown Role')} at {job_data.get('company', 'Unknown Company')}")
        
        # Extract job requirements
        job_requirements = self._extract_job_requirements(job_data)
        
        # Generate AI-powered customizations
        if self.openai_api_key and OPENAI_AVAILABLE:
            customization = self._ai_generate_customizations(job_data, job_requirements, company_intelligence)
        else:
            customization = self._basic_generate_customizations(job_data, job_requirements)
        
        # Store version for tracking
        version_key = f"{job_data.get('company', 'unknown')}_{job_data.get('title', 'role')}"
        self.resume_versions[version_key] = customization
        
        print(f"* Resume customization completed: {customization.version_name}")
        return customization
    
    def _extract_job_requirements(self, job_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract key requirements from job posting"""
        description = job_data.get('description', '').lower()
        requirements = job_data.get('requirements', [])
        
        # Technical skills extraction
        tech_keywords = {
            'programming': ['python', 'javascript', 'java', 'c++', 'go', 'ruby'],
            'ai_ml': ['machine learning', 'ai', 'artificial intelligence', 'deep learning', 'nlp', 'computer vision'],
            'automation': ['automation', 'scripting', 'ci/cd', 'devops', 'pipeline', 'workflow'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker'],
            'infrastructure': ['infrastructure', 'servers', 'networking', 'linux', 'windows'],
            'data': ['data analysis', 'data science', 'sql', 'databases', 'analytics']
        }
        
        found_skills = {}
        for category, keywords in tech_keywords.items():
            found_skills[category] = []
            for keyword in keywords:
                if keyword in description:
                    found_skills[category].append(keyword)
        
        return found_skills
    
    def _ai_generate_customizations(
        self, 
        job_data: Dict[str, Any], 
        requirements: Dict[str, List[str]], 
        company_intel: Optional[Dict] = None
    ) -> ResumeCustomization:
        """Use AI to generate intelligent resume customizations"""
        
        customization_prompt = self._build_customization_prompt(job_data, requirements, company_intel)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert resume optimization specialist helping an Infrastructure Engineer transition to AI/Automation roles. Provide specific, actionable customization advice."},
                    {"role": "user", "content": customization_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_ai_customization_response(ai_response, job_data)
            
        except Exception as e:
            print(f"! AI customization failed: {e}")
            return self._basic_generate_customizations(job_data, requirements)
    
    def _build_customization_prompt(self, job_data: Dict, requirements: Dict, company_intel: Optional[Dict]) -> str:
        """Build comprehensive customization prompt"""
        
        company_context = ""
        if company_intel:
            company_context = f"""
Company Intelligence:
- Industry: {company_intel.get('industry', 'N/A')}
- Culture: {', '.join(company_intel.get('culture_keywords', []))}
- Tech Stack: {', '.join(company_intel.get('tech_stack', []))}
- Recent News: {', '.join(company_intel.get('recent_news', [])[:2])}
"""
        
        prompt = f"""
Customize resume for Infrastructure Engineer to AI/Automation transition.

Job Details:
- Title: {job_data.get('title', 'N/A')}
- Company: {job_data.get('company', 'N/A')}
- Key Requirements: {requirements}

{company_context}

Current Profile Strengths:
- 99.8% uptime Infrastructure experience
- Python automation bot development
- GitHub API integration
- Production system reliability
- Systematic problem-solving approach

Please provide JSON response with:
{{
  "emphasized_skills": ["top 5 skills to emphasize from my profile"],
  "highlighted_achievements": ["top 3 achievements to highlight"],
  "customized_summary": "Tailored professional summary for this role",
  "keyword_optimization": ["5 keywords to ensure are included"],
  "culture_adaptations": ["3 ways to adapt for company culture"],
  "specific_positioning": "How to position Infrastructure to AI transition for this role"
}}

Focus on matching job requirements while maintaining authentic Infrastructure to AI narrative.
        """
        
        return prompt.strip()
    
    def _parse_ai_customization_response(self, ai_response: str, job_data: Dict) -> ResumeCustomization:
        """Parse AI customization response into structured data"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                customization_data = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
            
            return ResumeCustomization(
                job_title=job_data.get('title', 'Unknown Role'),
                company_name=job_data.get('company', 'Unknown Company'),
                emphasized_skills=customization_data.get('emphasized_skills', []),
                highlighted_achievements=customization_data.get('highlighted_achievements', []),
                customized_summary=customization_data.get('customized_summary', self.base_profile.professional_summary),
                keyword_optimization=customization_data.get('keyword_optimization', []),
                culture_adaptations=customization_data.get('culture_adaptations', []),
                version_name=f"{job_data.get('company', 'company')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
            )
            
        except Exception as e:
            print(f"! Failed to parse AI customization: {e}")
            return self._basic_generate_customizations(job_data, {})
    
    def _basic_generate_customizations(self, job_data: Dict, requirements: Dict) -> ResumeCustomization:
        """Fallback customization when AI is not available"""
        
        # Basic skill emphasis based on job title
        job_title_lower = job_data.get('title', '').lower()
        
        if 'ai' in job_title_lower or 'machine learning' in job_title_lower:
            emphasized_skills = ["Python Development & Automation", "Algorithm Development", "Data Processing", "API Integration", "Systematic Problem-Solving"]
        elif 'automation' in job_title_lower or 'devops' in job_title_lower:
            emphasized_skills = ["Python Development & Automation", "GitHub API Integration", "CI/CD Pipeline Understanding", "Process Optimization", "System Integration"]
        else:
            emphasized_skills = ["Infrastructure Management", "Python Automation", "System Reliability", "API Integration", "Technical Problem-Solving"]
        
        return ResumeCustomization(
            job_title=job_data.get('title', 'Unknown Role'),
            company_name=job_data.get('company', 'Unknown Company'),
            emphasized_skills=emphasized_skills,
            highlighted_achievements=self.base_profile.key_achievements[:3],
            customized_summary=self.base_profile.professional_summary,
            keyword_optimization=['python', 'automation', 'infrastructure', 'api', 'reliability'],
            culture_adaptations=['Emphasize learning mindset', 'Highlight systematic approach', 'Show innovation through projects'],
            version_name=f"{job_data.get('company', 'company')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        )
    
    def generate_resume_content(self, customization: ResumeCustomization) -> Dict[str, Any]:
        """Generate complete customized resume content"""
        print(f"* Generating resume content for {customization.company_name}")
        
        # Start with base profile
        profile = asdict(self.base_profile)
        
        # Apply customizations
        profile['professional_summary'] = customization.customized_summary
        profile['emphasized_skills'] = customization.emphasized_skills
        profile['highlighted_achievements'] = customization.highlighted_achievements
        profile['keyword_optimization'] = customization.keyword_optimization
        
        # Add customization metadata
        profile['customization'] = asdict(customization)
        profile['generated_at'] = datetime.now().isoformat()
        
        return profile
    
    def export_resume_markdown(self, customization: ResumeCustomization, filename: str = None) -> str:
        """Export customized resume as markdown"""
        if not filename:
            filename = f"resume_{customization.version_name}.md"
        
        content = self.generate_resume_content(customization)
        
        markdown_content = self._format_resume_markdown(content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"* Resume exported to: {filename}")
        return filename
    
    def _format_resume_markdown(self, content: Dict[str, Any]) -> str:
        """Format resume content as professional markdown"""
        
        md = f"""# {content['name']}
**{content['current_role']} to {content['target_role']}**

📍 {content['location']}  
📧 {content['email']}  
📱 {content['phone']}  
🔗 [Portfolio]({content['portfolio_url']}) | [GitHub]({content['github_url']}) | [LinkedIn]({content['linkedin_url']})

---

## PROFESSIONAL SUMMARY

{content['professional_summary']}

---

## EMPLOYMENT HISTORY

"""
        
        # Add work experience
        for job in content['work_experience']:
            md += f"""### {job['title']}
**{job['company']}** | {job['location']}  
*{job['duration']}*

"""
            for achievement in job['achievements']:
                md += f"- {achievement}\n"
            md += "\n"
        
        # Add projects
        md += "---\n\n## RECENT TRANSITION PROJECTS\n\n"
        for project in content['projects']:
            md += f"""### {project['name']}
**{project['description']}** | *{project['date']}*  
🔗 [Repository]({project['url']})

"""
            for detail in project['details']:
                md += f"- {detail}\n"
            md += f"- **Technologies:** {', '.join(project['technologies'])}\n\n"
        
        # Add technical skills
        md += "---\n\n## TECHNICAL SKILLS\n\n"
        for category, skills in content['technical_skills'].items():
            md += f"### {category}\n"
            for skill in skills:
                md += f"- {skill}\n"
            md += "\n"
        
        # Add education
        md += "---\n\n## EDUCATION\n\n"
        for edu in content['education']:
            md += f"### {edu['degree']}\n**{edu['institution']}**  \n*{edu['duration']}*\n\n"
        
        # Add certifications
        md += "---\n\n## CERTIFICATIONS & CONTINUED LEARNING\n\n"
        for cert in content['certifications']:
            md += f"- **{cert['name']}** - {cert['issuer']} ({cert['date']})\n"
        
        # Add achievements section
        md += "\n---\n\n## KEY ACHIEVEMENTS\n\n"
        for achievement in content['key_achievements']:
            md += f"- {achievement}\n"
        
        # Add customization footer
        customization = content.get('customization', {})
        if customization:
            md += f"\n---\n\n*Resume customized for {customization.get('job_title', 'N/A')} at {customization.get('company_name', 'N/A')} - Generated {content['generated_at'][:10]}*\n"
        
        return md
    
    def track_resume_performance(self, version_name: str, response_received: bool = False, interview_scheduled: bool = False):
        """Track performance of different resume versions"""
        if version_name in self.resume_versions:
            # This would integrate with application tracking system
            performance = {
                'version': version_name,
                'response_received': response_received,
                'interview_scheduled': interview_scheduled,
                'tracked_at': datetime.now().isoformat()
            }
            
            # Save performance data
            performance_file = f"resume_performance_{datetime.now().strftime('%Y%m')}.json"
            
            try:
                with open(performance_file, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            data.append(performance)
            
            with open(performance_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"📊 Resume performance tracked for {version_name}")

def test_resume_engine():
    """Test the enhanced resume engine"""
    print("🧪 Testing Enhanced Resume Engine")
    
    engine = EnhancedResumeEngine()
    
    # Test job data
    test_job = {
        'title': 'AI Engineer',
        'company': 'TechCorp',
        'description': 'We are looking for an AI Engineer with Python experience to build machine learning systems. Strong infrastructure background preferred.',
        'requirements': ['Python', 'Machine Learning', 'Infrastructure', 'APIs']
    }
    
    # Generate customization
    customization = engine.customize_resume_for_job(test_job)
    
    print(f"\n📊 Customization Results:")
    print(f"Version: {customization.version_name}")
    print(f"Emphasized Skills: {customization.emphasized_skills}")
    print(f"Keywords: {customization.keyword_optimization}")
    
    # Export resume
    filename = engine.export_resume_markdown(customization)
    print(f"\n*** Test completed. Resume exported to: {filename} ***")

if __name__ == "__main__":
    test_resume_engine()