#!/usr/bin/env python3
"""
AI Company Research Module
=========================

Enhanced company intelligence gathering using OpenAI for deep company research
and job-specific application optimization.

Features:
- Automated company background research
- Recent news and developments analysis  
- Company culture and values identification
- Technical stack and technology preferences
- Competitive landscape understanding
- AI-powered application customization recommendations
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re

# Optional OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI not installed. AI features will use fallback mode.")

@dataclass
class CompanyIntelligence:
    """Structured company research data"""
    name: str
    industry: str
    size: str
    location: str
    description: str
    recent_news: List[str]
    tech_stack: List[str]
    culture_keywords: List[str]
    values: List[str]
    competitors: List[str]
    job_fit_score: float
    application_recommendations: List[str]
    research_timestamp: str

class AICompanyResearcher:
    """
    AI-powered company research for job applications
    
    Uses OpenAI to analyze company data and generate personalized
    application strategies for Infrastructure to AI career transition.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize with OpenAI API key"""
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            print("Warning: No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
            print("Using basic research mode without AI enhancement.")
        
        # Configure OpenAI
        if self.openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_api_key
        
        # Company research cache (avoid duplicate API calls)
        self.research_cache = {}
        
    def research_company(self, company_name: str, job_title: str = None) -> CompanyIntelligence:
        """
        Comprehensive AI-powered company research
        
        Args:
            company_name: Target company name
            job_title: Optional job title for specific analysis
            
        Returns:
            CompanyIntelligence: Complete research package
        """
        print(f"* Starting AI-powered research for {company_name}")
        
        # Check cache first
        cache_key = f"{company_name}_{job_title}".lower()
        if cache_key in self.research_cache:
            print("📋 Using cached research data")
            return self.research_cache[cache_key]
        
        # Step 1: Basic company information
        basic_info = self._gather_basic_company_info(company_name)
        
        # Step 2: AI-enhanced analysis
        if self.openai_api_key and OPENAI_AVAILABLE:
            enhanced_info = self._ai_enhance_company_research(company_name, basic_info, job_title)
        else:
            enhanced_info = self._basic_company_analysis(basic_info)
        
        # Step 3: Generate application recommendations
        recommendations = self._generate_application_strategy(company_name, enhanced_info, job_title)
        
        # Build comprehensive intelligence
        intelligence = CompanyIntelligence(
            name=company_name,
            industry=enhanced_info.get('industry', 'Technology'),
            size=enhanced_info.get('size', 'Unknown'),
            location=enhanced_info.get('location', 'Various locations'),
            description=enhanced_info.get('description', ''),
            recent_news=enhanced_info.get('recent_news', []),
            tech_stack=enhanced_info.get('tech_stack', []),
            culture_keywords=enhanced_info.get('culture_keywords', []),
            values=enhanced_info.get('values', []),
            competitors=enhanced_info.get('competitors', []),
            job_fit_score=enhanced_info.get('job_fit_score', 7.5),
            application_recommendations=recommendations,
            research_timestamp=datetime.now().isoformat()
        )
        
        # Cache the results
        self.research_cache[cache_key] = intelligence
        
        print(f"* Company research completed for {company_name}")
        return intelligence
    
    def _gather_basic_company_info(self, company_name: str) -> Dict[str, Any]:
        """Gather basic company information from available sources"""
        print(f"* Gathering basic information for {company_name}")
        
        # This would integrate with various APIs and sources
        # For now, using AI-powered analysis as primary source
        basic_info = {
            'name': company_name,
            'description': f'Research target: {company_name}',
            'data_sources': ['ai_analysis', 'web_research']
        }
        
        return basic_info
    
    def _ai_enhance_company_research(self, company_name: str, basic_info: Dict, job_title: str = None) -> Dict[str, Any]:
        """Use OpenAI to enhance company research with deep analysis"""
        print(f"* AI-enhancing research for {company_name}")
        
        # Construct research prompt
        research_prompt = self._build_company_research_prompt(company_name, job_title)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert company researcher helping an Infrastructure Engineer transition to AI/Automation roles. Provide detailed, accurate company analysis."},
                    {"role": "user", "content": research_prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            ai_analysis = response.choices[0].message.content
            
            # Parse AI response into structured data
            enhanced_info = self._parse_ai_company_analysis(ai_analysis)
            
            return enhanced_info
            
        except Exception as e:
            print(f"! AI research failed: {e}")
            print("Falling back to basic analysis")
            return self._basic_company_analysis(basic_info)
    
    def _build_company_research_prompt(self, company_name: str, job_title: str = None) -> str:
        """Build comprehensive research prompt for OpenAI"""
        job_context = f" for a {job_title} position" if job_title else ""
        
        prompt = f"""
Research {company_name}{job_context} for a job application. I'm an Infrastructure Engineer with 99.8% uptime experience transitioning to AI/Automation roles.

Please provide a comprehensive analysis in JSON format:

{{
  "industry": "Primary industry/sector",
  "size": "Company size (startup/mid-size/enterprise)",
  "location": "Primary locations",
  "description": "2-3 sentence company overview",
  "recent_news": ["3-5 recent developments, funding, products, expansions"],
  "tech_stack": ["Key technologies they use - focus on Python, AI, automation, infrastructure"],
  "culture_keywords": ["5-8 keywords describing company culture"],
  "values": ["3-5 core company values or principles"],
  "competitors": ["3-5 main competitors"],
  "job_fit_score": 8.5,
  "infrastructure_relevance": "How my infrastructure background applies",
  "automation_opportunities": "Where my automation skills would be valuable",
  "ai_transition_fit": "How this role supports my AI career transition"
}}

Focus on information relevant to Infrastructure to AI career transition. Be specific about technologies, recent AI/automation initiatives, and infrastructure needs.
        """
        
        return prompt.strip()
    
    def _parse_ai_company_analysis(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response into structured company data"""
        try:
            # Extract JSON from AI response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Fallback parsing if JSON not properly formatted
                return self._fallback_parse_ai_response(ai_response)
                
        except json.JSONDecodeError:
            print("! Failed to parse AI response as JSON")
            return self._fallback_parse_ai_response(ai_response)
    
    def _fallback_parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Fallback parsing when JSON parsing fails"""
        return {
            'industry': 'Technology',
            'size': 'Mid-size',
            'description': ai_response[:200] + '...' if len(ai_response) > 200 else ai_response,
            'recent_news': ['AI research ongoing', 'Product development active'],
            'tech_stack': ['Python', 'Cloud platforms', 'APIs'],
            'culture_keywords': ['innovative', 'collaborative', 'growth-focused'],
            'values': ['Innovation', 'Excellence', 'Teamwork'],
            'competitors': ['Industry leaders'],
            'job_fit_score': 7.5
        }
    
    def _basic_company_analysis(self, basic_info: Dict) -> Dict[str, Any]:
        """Basic analysis when AI is not available"""
        return {
            'industry': 'Technology',
            'size': 'Unknown',
            'location': 'Various locations',
            'description': f"Target company: {basic_info.get('name', 'Unknown')}",
            'recent_news': ['Research in progress'],
            'tech_stack': ['Python', 'APIs', 'Cloud platforms'],
            'culture_keywords': ['innovative', 'technical', 'growth-focused'],
            'values': ['Innovation', 'Quality', 'Collaboration'],
            'competitors': ['Industry competitors'],
            'job_fit_score': 7.0
        }
    
    def _generate_application_strategy(self, company_name: str, company_info: Dict, job_title: str = None) -> List[str]:
        """Generate AI-powered application recommendations"""
        print(f"* Generating application strategy for {company_name}")
        
        if not self.openai_api_key:
            return self._basic_application_strategy(company_info)
        
        try:
            strategy_prompt = f"""
Based on this company research for {company_name}:
- Industry: {company_info.get('industry')}
- Tech Stack: {', '.join(company_info.get('tech_stack', []))}
- Culture: {', '.join(company_info.get('culture_keywords', []))}
- Recent News: {', '.join(company_info.get('recent_news', [])[:2])}

Job Title: {job_title or 'Technical role'}

I'm an Infrastructure Engineer (99.8% uptime) transitioning to AI/Automation with:
- Production Python automation bot development
- GitHub API integration experience  
- AI-powered content generation projects
- Strong infrastructure reliability background

Generate 5 specific application recommendations:
1. Resume customization advice
2. Cover letter key points
3. Specific technologies to emphasize
4. Company-specific value propositions
5. Interview preparation focus

Make recommendations specific to this company and role.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert career coach specializing in Infrastructure to AI role transitions. Provide specific, actionable advice."},
                    {"role": "user", "content": strategy_prompt}
                ],
                max_tokens=800,
                temperature=0.4
            )
            
            strategy = response.choices[0].message.content
            
            # Parse into list of recommendations
            recommendations = []
            lines = strategy.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•'))):
                    # Clean up the recommendation
                    clean_rec = re.sub(r'^[\d\.\-\•\s]+', '', line).strip()
                    if clean_rec:
                        recommendations.append(clean_rec)
            
            return recommendations[:5] if recommendations else self._basic_application_strategy(company_info)
            
        except Exception as e:
            print(f"! AI strategy generation failed: {e}")
            return self._basic_application_strategy(company_info)
    
    def _basic_application_strategy(self, company_info: Dict) -> List[str]:
        """Fallback application strategy when AI is not available"""
        return [
            "Emphasize infrastructure reliability (99.8% uptime) as foundation for AI system deployment",
            "Highlight Python automation bot development as evidence of programming capabilities",
            "Connect GitHub API integration experience to their technology stack",
            "Position infrastructure background as valuable for understanding AI system requirements",
            "Demonstrate learning mindset through documented transition to AI/automation"
        ]
    
    def get_personalized_talking_points(self, intelligence: CompanyIntelligence, job_title: str = None) -> List[str]:
        """Generate personalized talking points for this specific company"""
        talking_points = []
        
        # Infrastructure relevance
        talking_points.append(f"Infrastructure expertise: My 99.8% uptime experience provides the reliability foundation {intelligence.name} needs for scalable systems")
        
        # Technology alignment
        if intelligence.tech_stack:
            common_tech = [tech for tech in intelligence.tech_stack if tech.lower() in ['python', 'api', 'automation', 'cloud']]
            if common_tech:
                talking_points.append(f"Technology alignment: Production experience with {', '.join(common_tech)} directly matches your tech stack")
        
        # Culture fit
        if intelligence.culture_keywords:
            culture_match = [word for word in intelligence.culture_keywords if word.lower() in ['innovative', 'learning', 'growth', 'technical']]
            if culture_match:
                talking_points.append(f"Culture fit: My transition to AI demonstrates {', '.join(culture_match)} mindset that aligns with {intelligence.name}")
        
        # Company-specific value
        if intelligence.recent_news:
            talking_points.append(f"Timely contribution: With your recent developments in {intelligence.recent_news[0]}, my automation skills can help scale these initiatives")
        
        return talking_points
    
    def export_research(self, intelligence: CompanyIntelligence, filename: str = None) -> str:
        """Export research to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company_clean = re.sub(r'[^\w\s-]', '', intelligence.name).strip().replace(' ', '_')
            filename = f"company_research_{company_clean}_{timestamp}.json"
        
        research_data = {
            'company': intelligence.name,
            'research_data': intelligence.__dict__,
            'generated_at': intelligence.research_timestamp,
            'version': '1.0'
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)
        
        print(f"* Company research exported to: {filename}")
        return filename

def test_company_research():
    """Test the company research functionality"""
    print("*** Testing AI Company Research ***")
    
    researcher = AICompanyResearcher()
    
    # Test with a known tech company
    intelligence = researcher.research_company("OpenAI", "AI Engineer")
    
    print(f"\n* Research Results for {intelligence.name}:")
    print(f"Industry: {intelligence.industry}")
    print(f"Job Fit Score: {intelligence.job_fit_score}/10")
    print(f"Tech Stack: {', '.join(intelligence.tech_stack)}")
    print(f"Culture Keywords: {', '.join(intelligence.culture_keywords)}")
    
    print(f"\n* Application Recommendations:")
    for i, rec in enumerate(intelligence.application_recommendations, 1):
        print(f"  {i}. {rec}")
    
    # Export research
    filename = researcher.export_research(intelligence)
    print(f"\n* Research exported to: {filename}")

if __name__ == "__main__":
    test_company_research()