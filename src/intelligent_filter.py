#!/usr/bin/env python3
"""
Intelligent Job Filtering System
===============================

AI-powered job filtering with multi-dimensional analysis
and relevance scoring for Infrastructure → AI transition.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import json
import openai
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
import re
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScoringResult:
    """Comprehensive job opportunity scoring result"""
    overall_score: float  # 0-10 weighted average
    confidence_level: float  # 0-1 confidence in scoring
    technical_score: float  # 0-10 technical alignment
    transition_score: float  # 0-10 career transition fit
    culture_score: float  # 0-10 company culture match
    growth_score: float  # 0-10 growth potential
    compensation_score: float  # 0-10 compensation alignment
    reasoning: str  # AI explanation of scoring
    action_recommendation: str  # Next steps recommendation
    keywords_matched: List[str]  # Relevant keywords found
    red_flags: List[str]  # Potential concerns identified

class IntelligentFilter:
    """
    AI-powered job filtering with OpenAI integration
    
    Scoring Dimensions:
    - Technical Relevance (0-10)
    - Career Transition Fit (0-10)  
    - Company Culture Match (0-10)
    - Growth Potential (0-10)
    - Compensation Alignment (0-10)
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, fallback_mode: bool = False):
        self.openai_api_key = openai_api_key
        self.fallback_mode = fallback_mode
        self.client = None
        
        # Initialize OpenAI if API key available
        if openai_api_key and not fallback_mode:
            try:
                self.client = openai.OpenAI(api_key=openai_api_key)
                logger.info("OpenAI client initialized for intelligent filtering")
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}. Using fallback mode.")
                self.fallback_mode = True
        else:
            self.fallback_mode = True
            logger.info("Using fallback mode for job filtering")
        
        # Load scoring criteria and keywords
        self._load_scoring_criteria()
    
    def _load_scoring_criteria(self):
        """Load scoring criteria and keyword lists"""
        # Infrastructure to AI transition keywords
        self.ai_keywords = [
            'machine learning', 'ml', 'artificial intelligence', 'ai', 'deep learning',
            'neural networks', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas',
            'numpy', 'data science', 'nlp', 'computer vision', 'automation',
            'python', 'jupyter', 'model deployment', 'mlops', 'data pipeline'
        ]
        
        self.infrastructure_keywords = [
            'kubernetes', 'docker', 'aws', 'azure', 'gcp', 'terraform', 'ansible',
            'jenkins', 'ci/cd', 'devops', 'monitoring', 'prometheus', 'grafana',
            'linux', 'bash', 'networking', 'security', 'sre', 'site reliability'
        ]
        
        self.growth_keywords = [
            'startup', 'scale-up', 'learning', 'mentorship', 'training',
            'conference budget', 'education', 'certification', 'career development',
            'advancement', 'leadership', 'team lead', 'senior', 'principal'
        ]
        
        self.red_flag_keywords = [
            'unpaid', 'volunteer', 'commission only', 'no benefits',
            'long hours', 'weekend work', 'on-call 24/7', 'toxic',
            'high pressure', 'fast-paced environment'  # context-dependent
        ]
        
        # Scoring weights
        self.scoring_weights = {
            'technical': 0.40,
            'transition': 0.25,
            'culture': 0.20,
            'growth': 0.10,
            'compensation': 0.05
        }
    
    def score_opportunity(self, job_opportunity) -> ScoringResult:
        """
        Score a job opportunity using AI analysis or fallback rules
        """
        if not self.fallback_mode and self.client:
            return self._ai_score_opportunity(job_opportunity)
        else:
            return self._fallback_score_opportunity(job_opportunity)
    
    def _ai_score_opportunity(self, job) -> ScoringResult:
        """AI-powered job opportunity scoring using OpenAI"""
        try:
            # Prepare job data for AI analysis
            job_text = f"""
            Job Title: {job.title}
            Company: {job.company}
            Location: {job.location}
            Salary: {job.salary_range or 'Not specified'}
            Description: {job.description[:1500]}  # Limit for API efficiency
            Requirements: {' '.join(job.requirements[:10])}
            Technologies: {' '.join(job.technologies[:15])}
            """
            
            scoring_prompt = self._create_scoring_prompt(job_text)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert career transition advisor specializing in Infrastructure to AI/ML career moves. Provide detailed, actionable scoring and analysis."},
                    {"role": "user", "content": scoring_prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            # Parse AI response
            ai_analysis = response.choices[0].message.content
            return self._parse_ai_response(ai_analysis, job)
            
        except Exception as e:
            logger.error(f"AI scoring failed: {e}. Falling back to rule-based scoring.")
            return self._fallback_score_opportunity(job)
    
    def _create_scoring_prompt(self, job_text: str) -> str:
        """Create detailed scoring prompt for AI analysis"""
        return f"""
        Analyze this job opportunity for an Infrastructure Engineer transitioning to AI/ML:

        {job_text}

        CANDIDATE PROFILE:
        - 5+ years Infrastructure/DevOps experience (99.8% uptime track record)
        - Strong Python automation and system architecture skills
        - Currently building AI-powered job application automation
        - Seeking Infrastructure → AI transition roles
        - Values: Learning, growth, innovation, work-life balance

        SCORE (0-10) AND ANALYZE:

        1. TECHNICAL_SCORE: How well do infrastructure skills transfer to this AI role?
        2. TRANSITION_SCORE: Is this an ideal Infrastructure → AI bridge role?
        3. CULTURE_SCORE: Company culture fit for learning-focused professional?
        4. GROWTH_SCORE: Learning and advancement opportunities available?
        5. COMPENSATION_SCORE: Fair compensation for career transition context?

        PROVIDE JSON RESPONSE:
        {{
            "technical_score": X.X,
            "transition_score": X.X,
            "culture_score": X.X,
            "growth_score": X.X,
            "compensation_score": X.X,
            "confidence": 0.X,
            "keywords_matched": ["keyword1", "keyword2"],
            "red_flags": ["concern1", "concern2"],
            "reasoning": "Detailed explanation of scoring rationale",
            "recommendation": "APPLY/RESEARCH/PASS with specific next steps"
        }}
        """
    
    def _parse_ai_response(self, ai_response: str, job) -> ScoringResult:
        """Parse AI response into structured scoring result"""
        try:
            # Extract JSON from AI response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            json_str = ai_response[json_start:json_end]
            
            ai_data = json.loads(json_str)
            
            # Calculate weighted overall score
            overall_score = (
                ai_data.get('technical_score', 5.0) * self.scoring_weights['technical'] +
                ai_data.get('transition_score', 5.0) * self.scoring_weights['transition'] +
                ai_data.get('culture_score', 5.0) * self.scoring_weights['culture'] +
                ai_data.get('growth_score', 5.0) * self.scoring_weights['growth'] +
                ai_data.get('compensation_score', 5.0) * self.scoring_weights['compensation']
            )
            
            return ScoringResult(
                overall_score=round(overall_score, 1),
                confidence_level=ai_data.get('confidence', 0.8),
                technical_score=ai_data.get('technical_score', 5.0),
                transition_score=ai_data.get('transition_score', 5.0),
                culture_score=ai_data.get('culture_score', 5.0),
                growth_score=ai_data.get('growth_score', 5.0),
                compensation_score=ai_data.get('compensation_score', 5.0),
                reasoning=ai_data.get('reasoning', 'AI analysis completed'),
                action_recommendation=ai_data.get('recommendation', 'RESEARCH'),
                keywords_matched=ai_data.get('keywords_matched', []),
                red_flags=ai_data.get('red_flags', [])
            )
            
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return self._fallback_score_opportunity(job)
    
    def _fallback_score_opportunity(self, job) -> ScoringResult:
        """Rule-based fallback scoring when AI is unavailable"""
        logger.info(f"Using fallback scoring for: {job.title} at {job.company}")
        
        # Combine all text for analysis
        job_text = f"{job.title} {job.description} {' '.join(job.requirements)} {' '.join(job.technologies)}".lower()
        
        # Technical relevance scoring
        technical_score = self._score_technical_relevance(job_text)
        
        # Career transition fit
        transition_score = self._score_transition_fit(job_text, job.title)
        
        # Company culture (basic analysis)
        culture_score = self._score_company_culture(job_text)
        
        # Growth potential
        growth_score = self._score_growth_potential(job_text)
        
        # Compensation analysis
        compensation_score = self._score_compensation(job.salary_range, job_text)
        
        # Overall weighted score
        overall_score = (
            technical_score * self.scoring_weights['technical'] +
            transition_score * self.scoring_weights['transition'] +
            culture_score * self.scoring_weights['culture'] +
            growth_score * self.scoring_weights['growth'] +
            compensation_score * self.scoring_weights['compensation']
        )
        
        # Find matched keywords and red flags
        keywords_matched = [kw for kw in self.ai_keywords + self.infrastructure_keywords 
                          if kw in job_text]
        red_flags = [flag for flag in self.red_flag_keywords if flag in job_text]
        
        # Generate recommendation
        if overall_score >= 8.0:
            recommendation = "APPLY - High-priority opportunity"
        elif overall_score >= 6.0:
            recommendation = "RESEARCH - Investigate further"
        else:
            recommendation = "PASS - Focus on higher-scoring opportunities"
        
        reasoning = f"Rule-based analysis: Technical relevance {technical_score}/10, " \
                   f"Transition fit {transition_score}/10, Culture {culture_score}/10"
        
        return ScoringResult(
            overall_score=round(overall_score, 1),
            confidence_level=0.6,  # Lower confidence for rule-based
            technical_score=technical_score,
            transition_score=transition_score,
            culture_score=culture_score,
            growth_score=growth_score,
            compensation_score=compensation_score,
            reasoning=reasoning,
            action_recommendation=recommendation,
            keywords_matched=keywords_matched[:10],  # Limit for readability
            red_flags=red_flags
        )
    
    def _score_technical_relevance(self, job_text: str) -> float:
        """Score technical skill alignment (Infrastructure → AI)"""
        ai_matches = sum(1 for kw in self.ai_keywords if kw in job_text)
        infra_matches = sum(1 for kw in self.infrastructure_keywords if kw in job_text)
        
        # Ideal: High AI keywords + some infrastructure keywords for transition
        ai_score = min(ai_matches * 1.5, 7.0)  # Up to 7 points for AI keywords
        infra_bonus = min(infra_matches * 0.5, 3.0)  # Up to 3 bonus points for infra
        
        return min(ai_score + infra_bonus, 10.0)
    
    def _score_transition_fit(self, job_text: str, job_title: str) -> float:
        """Score career transition appropriateness"""
        # Look for transition-friendly terms
        transition_terms = ['junior', 'associate', 'entry', 'transition', 'bootcamp', 
                          'new grad', 'career change', 'infrastructure', 'devops to ai']
        
        # Senior roles that welcome transitions
        senior_but_open = ['senior devops', 'senior infrastructure', 'platform engineer',
                          'data platform', 'ml platform', 'ai platform']
        
        title_lower = job_title.lower()
        
        # Penalty for very senior AI roles without infrastructure component
        if any(term in title_lower for term in ['principal', 'staff', 'lead']) and \
           not any(term in title_lower for term in ['infrastructure', 'platform', 'devops']):
            return 3.0  # Too senior for transition
        
        # Bonus for explicit transition roles
        if any(term in job_text for term in transition_terms):
            return 9.0
        
        # Good for platform/infrastructure-adjacent AI roles
        if any(term in job_text for term in senior_but_open):
            return 8.0
        
        # Standard scoring based on keyword balance
        return 6.0  # Default for unclear transition fit
    
    def _score_company_culture(self, job_text: str) -> float:
        """Basic company culture assessment"""
        positive_culture = ['learning', 'growth', 'mentorship', 'collaboration',
                           'work-life balance', 'flexible', 'remote', 'innovative']
        negative_culture = ['fast-paced', 'high pressure', 'long hours', 'weekend work']
        
        positive_score = sum(2 for term in positive_culture if term in job_text)
        negative_penalty = sum(1 for term in negative_culture if term in job_text)
        
        base_score = 5.0 + positive_score - negative_penalty
        return max(min(base_score, 10.0), 1.0)
    
    def _score_growth_potential(self, job_text: str) -> float:
        """Score learning and advancement opportunities"""
        growth_indicators = sum(1 for kw in self.growth_keywords if kw in job_text)
        
        if growth_indicators >= 3:
            return 9.0
        elif growth_indicators >= 1:
            return 7.0
        else:
            return 5.0  # Default assumption
    
    def _score_compensation(self, salary_range: Optional[str], job_text: str) -> float:
        """Basic compensation analysis"""
        if not salary_range:
            return 5.0  # Unknown, assume average
        
        # Extract numbers from salary range
        numbers = re.findall(r'\d+', salary_range.replace(',', ''))
        if numbers:
            # Look for reasonable salary range for career transition
            valid_numbers = [int(num) for num in numbers if len(num) >= 4]  # 4+ digits
            
            if valid_numbers:
                max_salary = max(valid_numbers)
                
                if max_salary >= 120000:  # Good compensation
                    return 8.0
                elif max_salary >= 90000:  # Acceptable for transition
                    return 6.0
                elif max_salary >= 60000:  # Low but potentially acceptable
                    return 4.0
                else:
                    return 2.0  # Too low
        
        return 5.0  # Default if can't parse
    
    def rank_opportunities(self, jobs_with_scores: List[tuple]) -> List[tuple]:
        """
        Rank job opportunities by overall score with advanced logic
        
        Args:
            jobs_with_scores: List of (JobOpportunity, ScoringResult) tuples
            
        Returns:
            Sorted list prioritized by score and strategic factors
        """
        def ranking_key(job_score_pair):
            job, score = job_score_pair
            
            # Primary sort: Overall score
            primary_score = score.overall_score
            
            # Boost for high-confidence AI roles
            if score.confidence_level > 0.8 and score.technical_score >= 7.0:
                primary_score += 0.5
            
            # Boost for explicit Infrastructure → AI transition roles
            if score.transition_score >= 8.0:
                primary_score += 0.3
            
            # Penalty for red flags
            if score.red_flags:
                primary_score -= len(score.red_flags) * 0.2
            
            # Tie-breaker: Recent discovery (if available)
            recency_bonus = 0.01 if hasattr(job, 'discovered_at') else 0
            
            return -(primary_score + recency_bonus)  # Negative for descending sort
        
        ranked_jobs = sorted(jobs_with_scores, key=ranking_key)
        
        logger.info(f"Ranked {len(ranked_jobs)} job opportunities by score and strategic factors")
        return ranked_jobs

def test_intelligent_filter():
    """Test the intelligent filtering system"""
    print("\n" + "="*80)
    print("INTELLIGENT FILTER TESTING")
    print("="*80)
    
    # Create test job opportunity
    from job_discovery_engine import JobOpportunity
    from datetime import datetime
    import hashlib
    
    # Generate job_id
    unique_string = f"ml platform engineer_techstart ai_test"
    job_id = hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    test_job = JobOpportunity(
        title="ML Platform Engineer",
        company="TechStart AI",
        location="Remote",
        salary_range="$95,000 - $130,000",
        job_type="Full-time",
        source="test",
        discovered_at=datetime.now().isoformat(),
        url="https://test.com/job",
        job_id=job_id,
        description="Build and maintain ML infrastructure using Kubernetes, Python, and TensorFlow. Experience with AWS and DevOps practices preferred. Great learning environment with mentorship opportunities.",
        requirements=["Python", "Kubernetes", "AWS", "Machine Learning", "DevOps"],
        technologies=["TensorFlow", "Docker", "Jenkins", "Prometheus"]
    )
    
    # Test fallback mode
    filter_engine = IntelligentFilter(fallback_mode=True)
    result = filter_engine.score_opportunity(test_job)
    
    print(f"\nJob: {test_job.title} at {test_job.company}")
    print(f"Overall Score: {result.overall_score}/10 (Confidence: {result.confidence_level})")
    print(f"Technical: {result.technical_score}/10")
    print(f"Transition: {result.transition_score}/10")
    print(f"Culture: {result.culture_score}/10")
    print(f"Growth: {result.growth_score}/10")
    print(f"Compensation: {result.compensation_score}/10")
    print(f"\nReasoning: {result.reasoning}")
    print(f"Recommendation: {result.action_recommendation}")
    print(f"Keywords Matched: {result.keywords_matched[:5]}")
    if result.red_flags:
        print(f"Red Flags: {result.red_flags}")
    
    print("\n" + "="*80)
    print("INTELLIGENT FILTER TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    test_intelligent_filter()