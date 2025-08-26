#!/usr/bin/env python3
"""
Intelligent Cover Letter Generator
=================================

AI-powered cover letter generation with deep company research integration
and personalized value propositions for Infrastructure to AI career transition.

Features:
- Company-specific research integration
- Recent news and developments incorporation
- Technical skill matching and positioning  
- Culture-adapted tone and messaging
- Value proposition customization
- Multiple template styles (startup vs enterprise)
- A/B testing version management
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from ai_company_research import CompanyIntelligence

# Optional OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

@dataclass
class CoverLetterTemplate:
    """Cover letter template configuration"""
    name: str
    style: str  # 'professional', 'startup', 'technical', 'conversational'
    tone: str   # 'formal', 'friendly', 'direct', 'enthusiastic'
    structure: List[str]  # paragraph themes
    max_length: int

@dataclass
class CoverLetterGeneration:
    """Generated cover letter with metadata"""
    content: str
    company_name: str
    job_title: str
    template_used: str
    research_insights: List[str]
    value_propositions: List[str]
    personalization_score: float
    generated_at: str
    version_id: str

class IntelligentCoverLetterGenerator:
    """
    AI-powered cover letter generator with company intelligence
    
    Creates highly personalized cover letters by combining:
    - Your Infrastructure to AI transition story
    - Company-specific research and insights
    - Job requirement analysis
    - Cultural tone adaptation
    - Recent company developments
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize with OpenAI API key"""
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if self.openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_api_key
        
        # Load cover letter templates
        self.templates = self._load_templates()
        
        # Your professional profile for personalization
        self.profile = self._load_professional_profile()
        
        # Cover letter version tracking
        self.generated_letters = {}
    
    def _load_templates(self) -> Dict[str, CoverLetterTemplate]:
        """Load cover letter templates for different scenarios"""
        return {
            'ai_engineer_startup': CoverLetterTemplate(
                name='AI Engineer - Startup Focus',
                style='startup',
                tone='enthusiastic',
                structure=['hook_with_company_news', 'infrastructure_to_ai_story', 'technical_alignment', 'startup_value_add', 'growth_mindset_close'],
                max_length=350
            ),
            'ai_engineer_enterprise': CoverLetterTemplate(
                name='AI Engineer - Enterprise Focus', 
                style='professional',
                tone='formal',
                structure=['professional_opening', 'experience_credibility', 'technical_qualifications', 'enterprise_value', 'formal_close'],
                max_length=400
            ),
            'automation_engineer': CoverLetterTemplate(
                name='Automation Engineer',
                style='technical',
                tone='direct',
                structure=['automation_hook', 'infrastructure_foundation', 'python_automation_examples', 'process_optimization_value', 'technical_close'],
                max_length=375
            ),
            'devops_engineer': CoverLetterTemplate(
                name='DevOps Engineer',
                style='technical',
                tone='friendly',
                structure=['devops_evolution', 'infrastructure_reliability', 'automation_bridge', 'ci_cd_learning', 'collaboration_close'],
                max_length=350
            )
        }
    
    def _load_professional_profile(self) -> Dict[str, Any]:
        """Load your professional profile for personalization"""
        return {
            'name': 'Treyten Ellingson',
            'current_role': 'Infrastructure Engineer',
            'transition_goal': 'AI/Automation Engineer',
            'key_strengths': [
                '99.8% uptime infrastructure reliability',
                'Production Python automation development',
                'GitHub API integration and bot creation',
                'Systematic problem-solving approach',
                'Infrastructure to AI learning journey'
            ],
            'signature_projects': [
                'GitHub Development Logger Bot (Python, APIs, automation)',
                'Personal Portfolio with automated content integration',
                'Infrastructure monitoring achieving 99.8% uptime'
            ],
            'unique_value': 'Infrastructure reliability mindset applied to AI system development',
            'learning_evidence': 'Building production automation tools while maintaining operational excellence'
        }
    
    def generate_cover_letter(
        self, 
        job_data: Dict[str, Any],
        company_intelligence: Optional[CompanyIntelligence] = None,
        template_preference: Optional[str] = None
    ) -> CoverLetterGeneration:
        """
        Generate intelligent, personalized cover letter
        
        Args:
            job_data: Job posting information
            company_intelligence: AI-generated company research
            template_preference: Optional specific template to use
            
        Returns:
            CoverLetterGeneration: Complete generated cover letter with metadata
        """
        print(f"* Generating intelligent cover letter for {job_data.get('company', 'Unknown')} - {job_data.get('title', 'Unknown Role')}")
        
        # Select optimal template
        template_key = template_preference or self._select_optimal_template(job_data, company_intelligence)
        template = self.templates[template_key]
        
        print(f"* Using template: {template.name}")
        
        # Generate AI-powered cover letter
        if self.openai_api_key and OPENAI_AVAILABLE:
            letter_content = self._ai_generate_cover_letter(job_data, company_intelligence, template)
        else:
            letter_content = self._template_generate_cover_letter(job_data, company_intelligence, template)
        
        # Analyze and score the generated letter
        research_insights = self._extract_research_insights(company_intelligence)
        value_props = self._identify_value_propositions(letter_content)
        personalization_score = self._calculate_personalization_score(letter_content, company_intelligence)
        
        # Create generation object
        generation = CoverLetterGeneration(
            content=letter_content,
            company_name=job_data.get('company', 'Unknown Company'),
            job_title=job_data.get('title', 'Unknown Role'),
            template_used=template.name,
            research_insights=research_insights,
            value_propositions=value_props,
            personalization_score=personalization_score,
            generated_at=datetime.now().isoformat(),
            version_id=self._generate_version_id(job_data)
        )
        
        # Store for tracking
        self.generated_letters[generation.version_id] = generation
        
        print(f"* Cover letter generated with {personalization_score:.1f}/10 personalization score")
        return generation
    
    def _select_optimal_template(self, job_data: Dict, company_intel: Optional[CompanyIntelligence]) -> str:
        """Select the best template based on job and company analysis"""
        
        job_title = job_data.get('title', '').lower()
        job_description = job_data.get('description', '').lower()
        
        # Analyze company size/culture if available
        company_style = 'startup'
        if company_intel:
            if company_intel.size and 'enterprise' in company_intel.size.lower():
                company_style = 'enterprise'
            elif any(keyword in company_intel.culture_keywords for keyword in ['formal', 'corporate', 'traditional']):
                company_style = 'enterprise'
            elif any(keyword in company_intel.culture_keywords for keyword in ['startup', 'agile', 'fast-paced']):
                company_style = 'startup'
        
        # Template selection logic
        if 'ai engineer' in job_title or 'machine learning' in job_title:
            return 'ai_engineer_startup' if company_style == 'startup' else 'ai_engineer_enterprise'
        elif 'automation' in job_title:
            return 'automation_engineer'
        elif 'devops' in job_title:
            return 'devops_engineer'
        else:
            # Default to AI engineer template
            return 'ai_engineer_startup' if company_style == 'startup' else 'ai_engineer_enterprise'
    
    def _ai_generate_cover_letter(
        self, 
        job_data: Dict, 
        company_intel: Optional[CompanyIntelligence], 
        template: CoverLetterTemplate
    ) -> str:
        """Generate cover letter using OpenAI with company intelligence"""
        
        generation_prompt = self._build_generation_prompt(job_data, company_intel, template)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert cover letter writer specializing in Infrastructure to AI career transitions. Write compelling, personalized cover letters that showcase technical growth and genuine company fit."},
                    {"role": "user", "content": generation_prompt}
                ],
                max_tokens=800,
                temperature=0.4
            )
            
            cover_letter = response.choices[0].message.content.strip()
            
            # Clean up and format
            cover_letter = self._format_cover_letter(cover_letter, job_data)
            
            return cover_letter
            
        except Exception as e:
            print(f"! AI generation failed: {e}")
            print("Falling back to template generation")
            return self._template_generate_cover_letter(job_data, company_intel, template)
    
    def _build_generation_prompt(
        self, 
        job_data: Dict, 
        company_intel: Optional[CompanyIntelligence], 
        template: CoverLetterTemplate
    ) -> str:
        """Build comprehensive prompt for AI cover letter generation"""
        
        # Company context
        company_context = ""
        if company_intel:
            company_context = f"""
Company Intelligence:
- Industry: {company_intel.industry}
- Size: {company_intel.size}
- Culture: {', '.join(company_intel.culture_keywords[:5])}
- Tech Stack: {', '.join(company_intel.tech_stack[:6])}
- Recent News: {'; '.join(company_intel.recent_news[:2])}
- Values: {', '.join(company_intel.values[:3])}
"""
        
        # Job context
        job_requirements = []
        if job_data.get('requirements'):
            job_requirements = job_data['requirements'][:5]
        
        prompt = f"""
Write a compelling cover letter for Infrastructure Engineer to AI transition.

Job Details:
- Position: {job_data.get('title', 'AI Engineering Role')}
- Company: {job_data.get('company', 'Target Company')}
- Key Requirements: {', '.join(job_requirements)}

{company_context}

Candidate Profile (Infrastructure Engineer - Trey):
- Current: Infrastructure Engineer with 99.8% uptime track record
- Transition: Building AI/automation skills through hands-on projects
- Evidence: Production Python automation bot (GitHub API integration)
- Strength: Systematic problem-solving and reliability-first mindset
- Goal: Apply infrastructure stability to AI system development

Template Style: {template.style} ({template.tone} tone)
Structure: {' to '.join(template.structure)}
Length: {template.max_length} words maximum

Requirements:
1. Open with company-specific hook (use recent news/culture if available)
2. Position infrastructure experience as valuable for AI systems
3. Highlight specific Python automation accomplishments  
4. Show genuine interest in company's specific AI work
5. Close with clear value proposition

Make it authentic, specific, and compelling. Avoid generic phrases.
        """
        
        return prompt.strip()
    
    def _template_generate_cover_letter(
        self, 
        job_data: Dict, 
        company_intel: Optional[CompanyIntelligence], 
        template: CoverLetterTemplate
    ) -> str:
        """Fallback template-based generation when AI is not available"""
        
        company_name = job_data.get('company', 'your company')
        job_title = job_data.get('title', 'this position')
        
        # Company-specific opening
        opening = f"I'm excited to apply for the {job_title} position at {company_name}."
        if company_intel and company_intel.recent_news:
            opening = f"I was excited to read about {company_intel.recent_news[0]}. Your innovation in this space aligns perfectly with my transition from Infrastructure Engineering to AI/automation, and I'd love to contribute to the {job_title} role at {company_name}."
        
        # Core paragraphs based on template
        core_content = f"""
As an Infrastructure Engineer with 4+ years maintaining 99.8% uptime for enterprise systems, I bring a unique perspective to AI development: the reliability-first mindset essential for production AI systems.

My recent accomplishments demonstrate this infrastructure to AI transition:
• Built production-ready GitHub Development Logger Bot using Python and API integration
• Reduced operational workload by 40% through custom automation scripts  
• Developed systematic approaches to complex problem-solving that translate directly to AI challenges

What excites me about {company_name} is your commitment to {company_intel.values[0] if company_intel and company_intel.values else 'innovation'}. My infrastructure foundation provides the stability mindset your AI systems need, while my proven ability to learn and implement new technologies positions me to grow quickly in this role.
        """
        
        closing = f"I'd welcome the opportunity to discuss how my infrastructure reliability experience and emerging AI automation skills can contribute to {company_name}'s continued success."
        
        # Combine sections
        cover_letter = f"""Dear {company_name} Team,

{opening}

{core_content.strip()}

{closing}

Best regards,
Treyten Ellingson"""
        
        return cover_letter
    
    def _format_cover_letter(self, content: str, job_data: Dict) -> str:
        """Format and clean up the generated cover letter"""
        
        # Ensure proper structure
        if not content.startswith("Dear"):
            company_name = job_data.get('company', 'Hiring Manager')
            content = f"Dear {company_name} Team,\n\n{content}"
        
        if not content.endswith(("Best regards,\nTreyten Ellingson", "Sincerely,\nTreyten Ellingson")):
            content = f"{content}\n\nBest regards,\nTreyten Ellingson"
        
        # Clean up formatting
        content = re.sub(r'\n{3,}', '\n\n', content)  # Remove excessive line breaks
        content = re.sub(r'[ \t]+', ' ', content)  # Clean up spacing
        
        return content.strip()
    
    def _extract_research_insights(self, company_intel: Optional[CompanyIntelligence]) -> List[str]:
        """Extract key research insights used in the letter"""
        insights = []
        
        if company_intel:
            if company_intel.recent_news:
                insights.append(f"Recent development: {company_intel.recent_news[0]}")
            
            if company_intel.tech_stack:
                matching_tech = [tech for tech in company_intel.tech_stack if tech.lower() in ['python', 'api', 'automation']]
                if matching_tech:
                    insights.append(f"Tech alignment: {', '.join(matching_tech)}")
            
            if company_intel.culture_keywords:
                insights.append(f"Culture match: {', '.join(company_intel.culture_keywords[:3])}")
        
        return insights
    
    def _identify_value_propositions(self, letter_content: str) -> List[str]:
        """Identify key value propositions mentioned in the letter"""
        value_props = []
        
        content_lower = letter_content.lower()
        
        if '99.8%' in content_lower or 'uptime' in content_lower:
            value_props.append("Infrastructure reliability and uptime expertise")
        
        if 'python' in content_lower and ('automation' in content_lower or 'bot' in content_lower):
            value_props.append("Production Python automation development")
        
        if 'github' in content_lower and 'api' in content_lower:
            value_props.append("API integration and development experience")
        
        if 'systematic' in content_lower or 'problem-solving' in content_lower:
            value_props.append("Systematic problem-solving approach")
        
        if 'infrastructure' in content_lower and ('ai' in content_lower or 'automation' in content_lower):
            value_props.append("Infrastructure foundation for AI system development")
        
        return value_props
    
    def _calculate_personalization_score(
        self, 
        letter_content: str, 
        company_intel: Optional[CompanyIntelligence]
    ) -> float:
        """Calculate how personalized the cover letter is (0-10 scale)"""
        score = 5.0  # Base score
        
        content_lower = letter_content.lower()
        
        # Company-specific mentions
        if company_intel:
            if company_intel.name.lower() in content_lower:
                score += 1.0
            
            # Recent news integration
            if company_intel.recent_news:
                for news in company_intel.recent_news[:2]:
                    if any(word in content_lower for word in news.lower().split()[:3]):
                        score += 1.0
                        break
            
            # Tech stack alignment
            if company_intel.tech_stack:
                matching_tech = sum(1 for tech in company_intel.tech_stack if tech.lower() in content_lower)
                score += min(matching_tech * 0.5, 1.5)
            
            # Culture keywords
            if company_intel.culture_keywords:
                culture_matches = sum(1 for keyword in company_intel.culture_keywords if keyword.lower() in content_lower)
                score += min(culture_matches * 0.3, 1.0)
        
        # Specific achievements mentioned
        if '99.8%' in content_lower:
            score += 0.5
        if 'github' in content_lower and 'bot' in content_lower:
            score += 0.5
        if 'python' in content_lower and 'automation' in content_lower:
            score += 0.5
        
        return min(score, 10.0)
    
    def _generate_version_id(self, job_data: Dict) -> str:
        """Generate unique version ID for tracking"""
        company_clean = re.sub(r'[^\w\s-]', '', job_data.get('company', 'unknown')).strip().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"cover_letter_{company_clean}_{timestamp}"
    
    def export_cover_letter(self, generation: CoverLetterGeneration, filename: str = None) -> str:
        """Export cover letter to file"""
        if not filename:
            filename = f"{generation.version_id}.txt"
        
        # Create comprehensive output
        output = f"""COVER LETTER - {generation.company_name} - {generation.job_title}
{'='*60}

{generation.content}

{'='*60}
GENERATION METADATA:
Template Used: {generation.template_used}
Personalization Score: {generation.personalization_score:.1f}/10
Generated: {generation.generated_at[:19].replace('T', ' ')}

Research Insights Used:
{chr(10).join(f"• {insight}" for insight in generation.research_insights)}

Value Propositions Highlighted:
{chr(10).join(f"• {prop}" for prop in generation.value_propositions)}

Version ID: {generation.version_id}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"* Cover letter exported to: {filename}")
        return filename
    
    def analyze_letter_performance(self) -> Dict[str, Any]:
        """Analyze performance across all generated letters"""
        if not self.generated_letters:
            return {"message": "No letters generated yet"}
        
        letters = list(self.generated_letters.values())
        
        analysis = {
            'total_letters': len(letters),
            'average_personalization': sum(l.personalization_score for l in letters) / len(letters),
            'templates_used': {},
            'top_insights': {},
            'companies_targeted': len(set(l.company_name for l in letters))
        }
        
        # Template usage
        for letter in letters:
            template = letter.template_used
            analysis['templates_used'][template] = analysis['templates_used'].get(template, 0) + 1
        
        # Most common insights
        all_insights = []
        for letter in letters:
            all_insights.extend(letter.research_insights)
        
        for insight in all_insights:
            analysis['top_insights'][insight] = analysis['top_insights'].get(insight, 0) + 1
        
        return analysis

def test_cover_letter_generator():
    """Test the intelligent cover letter generator"""
    print("🧪 Testing Intelligent Cover Letter Generator")
    
    generator = IntelligentCoverLetterGenerator()
    
    # Test job data
    test_job = {
        'title': 'AI Engineer',
        'company': 'TechCorp AI',
        'description': 'We are seeking an AI Engineer to build machine learning systems. Infrastructure experience is a plus.',
        'requirements': ['Python', 'Machine Learning', 'System Design', 'APIs']
    }
    
    # Mock company intelligence
    from ai_company_research import CompanyIntelligence
    mock_intel = CompanyIntelligence(
        name='TechCorp AI',
        industry='Artificial Intelligence',
        size='Mid-size startup',
        location='San Francisco',
        description='Leading AI company building next-generation ML systems',
        recent_news=['Raised $50M Series B', 'Launched new AI platform'],
        tech_stack=['Python', 'PyTorch', 'Kubernetes', 'AWS'],
        culture_keywords=['innovative', 'collaborative', 'fast-paced', 'learning-oriented'],
        values=['Innovation', 'Excellence', 'Teamwork'],
        competitors=['OpenAI', 'Anthropic'],
        job_fit_score=8.5,
        application_recommendations=['Emphasize Python experience', 'Highlight infrastructure background'],
        research_timestamp=datetime.now().isoformat()
    )
    
    # Generate cover letter
    generation = generator.generate_cover_letter(test_job, mock_intel)
    
    print(f"\n📊 Generated Cover Letter:")
    print(f"Template: {generation.template_used}")
    print(f"Personalization Score: {generation.personalization_score:.1f}/10")
    print(f"\nContent Preview:")
    print(generation.content[:300] + "...")
    
    # Export letter
    filename = generator.export_cover_letter(generation)
    print(f"\n*** Test completed. Cover letter exported to: {filename} ***")

if __name__ == "__main__":
    test_cover_letter_generator()