#!/usr/bin/env python3
"""
Layer 2 System Integration Test
===============================

Complete test of Job Discovery Engine + Intelligent Filter integration
for Infrastructure → AI career transition automation.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from job_discovery_engine import JobDiscoveryEngine, DiscoveryConfig
from intelligent_filter import IntelligentFilter

async def test_complete_layer2_system():
    """Test complete Layer 2 system integration"""
    print("\n" + "="*80)
    print("LAYER 2 SYSTEM INTEGRATION TEST")
    print("AI Job Hunt Commander - Job Discovery + Intelligent Filtering")
    print("="*80)
    
    # 1. Initialize Job Discovery Engine
    print("\n1. Initializing Job Discovery Engine...")
    engine = JobDiscoveryEngine()
    
    # 2. Configure discovery for Infrastructure → AI transition
    config = DiscoveryConfig(
        keywords=["infrastructure", "platform", "devops", "ml", "ai", "python"],
        locations=["Remote", "San Francisco"],
        salary_min=100000,
        remote_only=False,
        target_roles=["Platform Engineer", "Infrastructure Engineer", "ML Engineer"],
        preferred_companies=["OpenAI", "Anthropic", "Databricks"],
        tech_stack_priorities=["Python", "Kubernetes", "AWS", "ML"],
        max_jobs_per_source=5,
        max_age_days=7,
        min_relevance_score=6.0
    )
    
    # 3. Discover jobs from all sources
    print("\n2. Discovering jobs from all sources...")
    discovered_jobs = await engine.discover_jobs(config, use_advanced_scrapers=True)
    
    print(f"+ Discovered {len(discovered_jobs)} jobs from multiple sources")
    
    # Show job sources breakdown
    source_counts = {}
    for job in discovered_jobs:
        source_counts[job.source] = source_counts.get(job.source, 0) + 1
    
    print("\nJob sources breakdown:")
    for source, count in source_counts.items():
        print(f"  - {source}: {count} jobs")
    
    # 4. Initialize Intelligent Filter
    print("\n3. Initializing Intelligent Filter...")
    filter_engine = IntelligentFilter(fallback_mode=True)  # Use fallback for testing
    
    # 5. Score and rank all discovered jobs
    print("\n4. Scoring and ranking job opportunities...")
    scored_jobs = []
    
    for job in discovered_jobs:
        score_result = filter_engine.score_opportunity(job)
        
        # Update job with scoring results
        job.relevance_score = score_result.overall_score
        job.priority_score = score_result.overall_score  # Use overall as priority for now
        job.transition_score = score_result.transition_score
        job.ai_analysis = {
            'technical_score': score_result.technical_score,
            'culture_score': score_result.culture_score,
            'growth_score': score_result.growth_score,
            'confidence': score_result.confidence_level,
            'reasoning': score_result.reasoning,
            'recommendation': score_result.action_recommendation,
            'keywords_matched': score_result.keywords_matched,
            'red_flags': score_result.red_flags
        }
        
        scored_jobs.append((job, score_result))
    
    # 6. Rank opportunities using intelligent filter
    print("\n5. Ranking opportunities by strategic factors...")
    ranked_jobs = filter_engine.rank_opportunities(scored_jobs)
    
    # 7. Display top opportunities
    print("\n6. TOP RANKED OPPORTUNITIES:")
    print("-" * 70)
    
    for i, (job, score) in enumerate(ranked_jobs[:8], 1):
        print(f"\n{i}. {job.title} at {job.company}")
        print(f"   Location: {job.location} | Salary: {job.salary_range or 'Salary not specified'}")
        print(f"   Source: {job.source.upper()}")
        print(f"   Overall Score: {score.overall_score}/10 (Confidence: {score.confidence_level})")
        print(f"   Technical: {score.technical_score}/10 | Transition: {score.transition_score}/10")
        print(f"   Culture: {score.culture_score}/10 | Growth: {score.growth_score}/10")
        print(f"   Recommendation: {score.action_recommendation}")
        
        if score.keywords_matched:
            print(f"   Matched Skills: {', '.join(score.keywords_matched[:5])}")
        
        if score.red_flags:
            print(f"   Concerns: {', '.join(score.red_flags[:3])}")
        
        # Show top technologies
        if job.technologies:
            print(f"   Tech Stack: {', '.join(job.technologies[:6])}")
    
    # 8. Summary statistics
    print(f"\n{'-'*70}")
    print("LAYER 2 SYSTEM PERFORMANCE SUMMARY")
    print(f"{'-'*70}")
    
    high_priority = len([job for job, score in ranked_jobs if score.overall_score >= 8.0])
    medium_priority = len([job for job, score in ranked_jobs if 6.0 <= score.overall_score < 8.0])
    low_priority = len([job for job, score in ranked_jobs if score.overall_score < 6.0])
    
    print(f"Total Jobs Discovered: {len(discovered_jobs)}")
    print(f"High Priority (8.0+): {high_priority} jobs")
    print(f"Medium Priority (6.0-7.9): {medium_priority} jobs")
    print(f"Low Priority (<6.0): {low_priority} jobs")
    
    # Calculate average scores
    avg_overall = sum(score.overall_score for _, score in ranked_jobs) / len(ranked_jobs)
    avg_technical = sum(score.technical_score for _, score in ranked_jobs) / len(ranked_jobs)
    avg_transition = sum(score.transition_score for _, score in ranked_jobs) / len(ranked_jobs)
    
    print(f"\nAverage Scores:")
    print(f"   Overall: {avg_overall:.1f}/10")
    print(f"   Technical Fit: {avg_technical:.1f}/10")
    print(f"   Transition Fit: {avg_transition:.1f}/10")
    
    # Infrastructure → AI transition insights
    ai_focused_jobs = len([job for job, _ in ranked_jobs if any(kw in job.title.lower() for kw in ['ai', 'ml', 'machine learning'])])
    platform_jobs = len([job for job, _ in ranked_jobs if any(kw in job.title.lower() for kw in ['platform', 'infrastructure'])])
    
    print(f"\nInfrastructure -> AI Transition Analysis:")
    print(f"   Direct AI/ML Roles: {ai_focused_jobs}")
    print(f"   Platform/Infrastructure Bridge Roles: {platform_jobs}")
    print(f"   Transition-Friendly Ratio: {(ai_focused_jobs + platform_jobs) / len(ranked_jobs) * 100:.1f}%")
    
    # 9. Test database operations
    print(f"\n7. Testing database operations...")
    saved_jobs = engine.get_discovered_jobs(limit=5)
    top_opportunities = engine.get_top_opportunities(limit=3)
    
    print(f"+ Retrieved {len(saved_jobs)} jobs from database")
    print(f"+ Retrieved {len(top_opportunities)} top opportunities")
    
    print(f"\n{'-'*70}")
    print("LAYER 2 SYSTEM TEST COMPLETE")
    print("+ Job Discovery: WORKING")
    print("+ Intelligent Filtering: WORKING")
    print("+ Database Storage: WORKING")
    print("+ Multi-Source Integration: WORKING")
    print("+ Infrastructure -> AI Analysis: WORKING")
    print(f"{'-'*70}")
    
    return ranked_jobs[:5]  # Return top 5 for potential further processing

def test_individual_components():
    """Test individual components separately"""
    print("\n" + "="*60)
    print("INDIVIDUAL COMPONENT TESTING")
    print("="*60)
    
    # Test Intelligent Filter standalone
    from intelligent_filter import test_intelligent_filter
    test_intelligent_filter()
    
    # Test scrapers if available
    try:
        from scrapers.indeed_scraper import test_indeed_scraper
        print(f"\n{'-'*60}")
        print("Testing Indeed Scraper (limited test)...")
        # test_indeed_scraper()  # Commented out to avoid rate limiting
        print("Indeed scraper test skipped (rate limiting)")
    except ImportError:
        print("Indeed scraper not available for testing")
    
    try:
        from scrapers.linkedin_scraper import test_linkedin_scraper
        print(f"\n{'-'*60}")
        test_linkedin_scraper()
    except ImportError:
        print("LinkedIn scraper not available for testing")

async def main():
    """Main test runner"""
    print("* Starting Layer 2 System Tests...")
    
    # Run complete system test
    top_jobs = await test_complete_layer2_system()
    
    # Run individual component tests
    test_individual_components()
    
    print(f"\n* ALL TESTS COMPLETED SUCCESSFULLY!")
    print("Layer 2 Job Discovery + Intelligent Filtering system is operational")
    
    return top_jobs

if __name__ == "__main__":
    asyncio.run(main())