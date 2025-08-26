#!/usr/bin/env python3
"""
Job Discovery Engine - Layer 2 Core Component
=============================================

Multi-source job aggregation and discovery system for AI Job Hunt Commander.
Designed for Infrastructure → AI career transition with intelligent filtering.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
Phase: Layer 2 - Advanced Job Search Automation
"""

import asyncio
import aiohttp
import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3
import logging
import sys
import os

# Add scrapers to path
scrapers_path = Path(__file__).parent / "scrapers"
if str(scrapers_path) not in sys.path:
    sys.path.append(str(scrapers_path))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JobOpportunity:
    """Structured job opportunity data"""
    # Basic Information
    title: str
    company: str
    location: str
    salary_range: Optional[str]
    job_type: str  # full-time, contract, remote
    
    # Discovery Metadata
    source: str  # indeed, linkedin, company, hn_jobs
    discovered_at: str
    url: str
    job_id: str  # unique identifier
    
    # Content Analysis
    description: str
    requirements: List[str]
    technologies: List[str]
    
    # AI Scoring (populated by intelligent_filter)
    relevance_score: float = 0.0  # 0-10 Infrastructure → AI fit
    priority_score: float = 0.0   # 0-10 application priority
    transition_score: float = 0.0 # 0-10 career transition alignment
    
    # Processing Status
    status: str = 'discovered'  # discovered, filtered, applied, rejected
    ai_analysis: Optional[Dict] = None
    application_package: Optional[str] = None

@dataclass
class DiscoveryConfig:
    """Configuration for job discovery parameters"""
    # Search Parameters
    keywords: List[str]
    locations: List[str]
    salary_min: Optional[int]
    remote_only: bool
    
    # Infrastructure → AI Transition Focus
    target_roles: List[str]
    preferred_companies: List[str]
    tech_stack_priorities: List[str]
    
    # Discovery Limits
    max_jobs_per_source: int
    max_age_days: int
    min_relevance_score: float

class JobDatabase:
    """SQLite database for job opportunity storage and management"""
    
    def __init__(self, db_path: str = "job_opportunities.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_opportunities (
                    job_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    salary_range TEXT,
                    job_type TEXT,
                    source TEXT NOT NULL,
                    discovered_at TEXT NOT NULL,
                    url TEXT NOT NULL,
                    description TEXT,
                    requirements TEXT,  -- JSON array
                    technologies TEXT,  -- JSON array
                    relevance_score REAL DEFAULT 0.0,
                    priority_score REAL DEFAULT 0.0,
                    transition_score REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'discovered',
                    ai_analysis TEXT,   -- JSON
                    application_package TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_relevance_score 
                ON job_opportunities(relevance_score DESC)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_discovered_at 
                ON job_opportunities(discovered_at DESC)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_status 
                ON job_opportunities(status)
            """)
    
    def save_job(self, job: JobOpportunity) -> bool:
        """Save job opportunity to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO job_opportunities 
                    (job_id, title, company, location, salary_range, job_type,
                     source, discovered_at, url, description, requirements, 
                     technologies, relevance_score, priority_score, transition_score,
                     status, ai_analysis, application_package)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.job_id, job.title, job.company, job.location,
                    job.salary_range, job.job_type, job.source, job.discovered_at,
                    job.url, job.description, json.dumps(job.requirements),
                    json.dumps(job.technologies), job.relevance_score,
                    job.priority_score, job.transition_score, job.status,
                    json.dumps(job.ai_analysis) if job.ai_analysis else None,
                    job.application_package
                ))
                return True
        except Exception as e:
            logger.error(f"Error saving job {job.job_id}: {e}")
            return False
    
    def get_jobs_by_status(self, status: str, limit: Optional[int] = None) -> List[JobOpportunity]:
        """Retrieve jobs by status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT * FROM job_opportunities 
                    WHERE status = ? 
                    ORDER BY relevance_score DESC, discovered_at DESC
                """
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor = conn.execute(query, (status,))
                return [self._row_to_job(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error retrieving jobs by status {status}: {e}")
            return []
    
    def get_top_opportunities(self, limit: int = 20) -> List[JobOpportunity]:
        """Get top-scored job opportunities"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM job_opportunities 
                    WHERE status = 'discovered' AND relevance_score > 0
                    ORDER BY relevance_score DESC, priority_score DESC
                    LIMIT ?
                """, (limit,))
                return [self._row_to_job(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error retrieving top opportunities: {e}")
            return []
    
    def _row_to_job(self, row) -> JobOpportunity:
        """Convert database row to JobOpportunity object"""
        return JobOpportunity(
            title=row[1], company=row[2], location=row[3],
            salary_range=row[4], job_type=row[5], source=row[6],
            discovered_at=row[7], url=row[8], job_id=row[0],
            description=row[9], 
            requirements=json.loads(row[10]) if row[10] else [],
            technologies=json.loads(row[11]) if row[11] else [],
            relevance_score=row[12], priority_score=row[13], transition_score=row[14],
            status=row[15], 
            ai_analysis=json.loads(row[16]) if row[16] else None,
            application_package=row[17]
        )

class BaseScraper:
    """Base class for job site scrapers"""
    
    def __init__(self, name: str, base_url: str, rate_limit: float = 1.0):
        self.name = name
        self.base_url = base_url
        self.rate_limit = rate_limit  # seconds between requests
        self.last_request = 0
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _rate_limited_request(self, url: str, **kwargs) -> Optional[str]:
        """Make rate-limited HTTP request"""
        # Rate limiting
        now = time.time()
        time_since_last = now - self.last_request
        if time_since_last < self.rate_limit:
            await asyncio.sleep(self.rate_limit - time_since_last)
        
        try:
            async with self.session.get(url, **kwargs) as response:
                self.last_request = time.time()
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"{self.name}: HTTP {response.status} for {url}")
                    return None
        except Exception as e:
            logger.error(f"{self.name}: Request failed for {url}: {e}")
            return None
    
    def _generate_job_id(self, title: str, company: str, source: str) -> str:
        """Generate unique job ID"""
        unique_string = f"{title.lower()}_{company.lower()}_{source}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    async def search_jobs(self, config: DiscoveryConfig) -> List[JobOpportunity]:
        """Override in subclasses"""
        raise NotImplementedError

class HackerNewsJobsScraper(BaseScraper):
    """Hacker News 'Who's Hiring' thread scraper for tech jobs"""
    
    def __init__(self):
        super().__init__("HackerNews", "https://hacker-news.firebaseio.com/v0", 0.1)
    
    async def search_jobs(self, config: DiscoveryConfig) -> List[JobOpportunity]:
        """Search latest Hacker News jobs thread"""
        jobs = []
        
        try:
            # Get latest "Who's Hiring" thread (simplified for demo)
            logger.info("Searching Hacker News jobs...")
            
            # For demo, create sample tech jobs focused on Infrastructure → AI transition
            sample_jobs = [
                {
                    "title": "Senior Infrastructure Engineer - AI Platform",
                    "company": "OpenAI",
                    "location": "San Francisco, CA / Remote",
                    "description": "Build and scale infrastructure for AI model training and deployment. Looking for SRE background with interest in AI/ML systems.",
                    "requirements": ["Python", "Kubernetes", "Infrastructure", "SRE", "AI/ML interest"],
                    "technologies": ["Python", "Kubernetes", "Terraform", "AWS", "ML Infrastructure"]
                },
                {
                    "title": "DevOps Engineer - ML Infrastructure",
                    "company": "Anthropic",
                    "location": "San Francisco, CA",
                    "description": "Scale ML training infrastructure and model deployment systems. Infrastructure engineering experience preferred.",
                    "requirements": ["DevOps", "Python", "Cloud Infrastructure", "Machine Learning"],
                    "technologies": ["Python", "Docker", "Kubernetes", "GCP", "MLOps"]
                },
                {
                    "title": "Site Reliability Engineer - AI Systems",
                    "company": "Scale AI", 
                    "location": "San Francisco, CA",
                    "description": "Ensure reliability and performance of AI training and inference systems. SRE experience with interest in AI applications.",
                    "requirements": ["SRE", "Python", "Monitoring", "Infrastructure", "AI Systems"],
                    "technologies": ["Python", "Prometheus", "Grafana", "Kubernetes", "AI/ML"]
                }
            ]
            
            for i, job_data in enumerate(sample_jobs):
                job = JobOpportunity(
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    salary_range="$150k - $220k",
                    job_type="full-time",
                    source="hn_jobs",
                    discovered_at=datetime.now().isoformat(),
                    url=f"https://news.ycombinator.com/item?id=demo_{i}",
                    job_id=self._generate_job_id(job_data["title"], job_data["company"], "hn_jobs"),
                    description=job_data["description"],
                    requirements=job_data["requirements"],
                    technologies=job_data["technologies"]
                )
                jobs.append(job)
                
            logger.info(f"Found {len(jobs)} jobs from Hacker News")
            
        except Exception as e:
            logger.error(f"HackerNews search failed: {e}")
        
        return jobs

class CompanyScraper(BaseScraper):
    """Direct company career page scraper"""
    
    def __init__(self):
        super().__init__("CompanyDirect", "https://", 2.0)  # Higher rate limit for politeness
    
    async def search_jobs(self, config: DiscoveryConfig) -> List[JobOpportunity]:
        """Search company career pages for AI/Infrastructure roles"""
        jobs = []
        
        # Target companies known for Infrastructure → AI opportunities
        target_companies = [
            ("Databricks", "https://databricks.com/careers"),
            ("Snowflake", "https://careers.snowflake.com/"),
            ("Terraform", "https://www.hashicorp.com/careers"),
        ]
        
        try:
            logger.info("Searching company career pages...")
            
            # For demo, create sample company jobs
            sample_jobs = [
                {
                    "title": "Infrastructure Automation Engineer",
                    "company": "Databricks",
                    "location": "Remote",
                    "description": "Build automation tools for ML infrastructure. Background in infrastructure engineering preferred with interest in ML/AI systems.",
                    "requirements": ["Python", "Infrastructure", "Automation", "Cloud", "ML Interest"],
                    "technologies": ["Python", "Terraform", "AWS", "Kubernetes", "Spark"]
                },
                {
                    "title": "Platform Engineer - Data Infrastructure", 
                    "company": "Snowflake",
                    "location": "San Mateo, CA / Remote",
                    "description": "Scale data platform infrastructure with ML/AI capabilities. Infrastructure engineering experience with data systems preferred.",
                    "requirements": ["Platform Engineering", "Python", "Data Systems", "Infrastructure"],
                    "technologies": ["Python", "SQL", "Kubernetes", "Cloud Platforms", "Data Engineering"]
                }
            ]
            
            for i, job_data in enumerate(sample_jobs):
                job = JobOpportunity(
                    title=job_data["title"],
                    company=job_data["company"], 
                    location=job_data["location"],
                    salary_range="$140k - $200k",
                    job_type="full-time",
                    source="company",
                    discovered_at=datetime.now().isoformat(),
                    url=f"https://{job_data['company'].lower()}.com/careers/demo_{i}",
                    job_id=self._generate_job_id(job_data["title"], job_data["company"], "company"),
                    description=job_data["description"],
                    requirements=job_data["requirements"],
                    technologies=job_data["technologies"]
                )
                jobs.append(job)
            
            logger.info(f"Found {len(jobs)} jobs from company sites")
            
        except Exception as e:
            logger.error(f"Company search failed: {e}")
        
        return jobs

class JobDiscoveryEngine:
    """Main job discovery coordination engine"""
    
    def __init__(self, db_path: str = "job_opportunities.db"):
        self.database = JobDatabase(db_path)
        
        # Initialize scrapers with error handling for imports
        self.scrapers = [
            HackerNewsJobsScraper(),
            CompanyScraper(),
        ]
        
        # Try to load advanced scrapers
        try:
            from indeed_scraper import IndeedScraper, IndeedSearchParams
            from linkedin_scraper import LinkedInScraper, LinkedInSearchParams
            self.indeed_scraper = IndeedScraper(rate_limit_delay=2.0)
            self.linkedin_scraper = LinkedInScraper(rate_limit_delay=3.0)
            self.advanced_scrapers_available = True
            logger.info("Advanced scrapers (Indeed, LinkedIn) loaded successfully")
        except ImportError as e:
            self.indeed_scraper = None
            self.linkedin_scraper = None
            self.advanced_scrapers_available = False
            logger.warning(f"Advanced scrapers not available: {e}")
        
        # Store scraper configs for advanced scrapers
        self.scraper_configs = {}
        
        # Default configuration for Infrastructure → AI transition
        self.default_config = DiscoveryConfig(
            keywords=["infrastructure", "devops", "sre", "platform", "automation", "ai", "ml", "python"],
            locations=["San Francisco", "Remote", "Seattle", "New York"],
            salary_min=120000,
            remote_only=False,
            target_roles=[
                "Infrastructure Engineer", "DevOps Engineer", "SRE", 
                "Platform Engineer", "Automation Engineer", "AI Infrastructure"
            ],
            preferred_companies=[
                "OpenAI", "Anthropic", "Scale AI", "Databricks", "Snowflake",
                "HashiCorp", "MongoDB", "Stripe", "Airbnb"
            ],
            tech_stack_priorities=["Python", "Kubernetes", "Terraform", "AWS", "ML", "AI"],
            max_jobs_per_source=10,
            max_age_days=7,
            min_relevance_score=6.0
        )
    
    async def discover_jobs(self, config: Optional[DiscoveryConfig] = None, use_advanced_scrapers: bool = True) -> List[JobOpportunity]:
        """Discover jobs from all configured sources"""
        if config is None:
            config = self.default_config
        
        all_jobs = []
        
        # Run basic scrapers concurrently
        scraper_tasks = []
        for scraper in self.scrapers:
            async with scraper:
                task = scraper.search_jobs(config)
                scraper_tasks.append(task)
        
        # Add advanced scrapers if available and requested
        advanced_tasks = []
        if use_advanced_scrapers and self.advanced_scrapers_available:
            advanced_tasks.extend(await self._run_advanced_scrapers(config))
        
        # Wait for all scrapers to complete
        all_tasks = scraper_tasks + advanced_tasks
        scraper_results = await asyncio.gather(*all_tasks, return_exceptions=True)
        
        # Collect results
        for result in scraper_results:
            if isinstance(result, Exception):
                logger.error(f"Scraper failed: {result}")
            else:
                if isinstance(result, list):
                    all_jobs.extend(result)
        
        # Remove duplicates based on job_id
        unique_jobs = self._deduplicate_jobs(all_jobs)
        
        # Save discovered jobs to database
        for job in unique_jobs:
            self.database.save_job(job)
        
        logger.info(f"Discovered {len(unique_jobs)} unique jobs across all sources")
        return unique_jobs
    
    async def _run_advanced_scrapers(self, config: DiscoveryConfig) -> List:
        """Run Indeed and LinkedIn scrapers"""
        advanced_tasks = []
        
        try:
            # Configure Indeed search
            if self.indeed_scraper:
                from indeed_scraper import IndeedSearchParams
                indeed_params = IndeedSearchParams(
                    keywords=" ".join(config.keywords[:3]),  # Limit keywords for API efficiency
                    location=config.locations[0] if config.locations else "Remote",
                    job_type="fulltime",
                    salary_min=config.salary_min,
                    remote_jobs=config.remote_only,
                    date_posted="7"
                )
                indeed_task = asyncio.create_task(self._run_indeed_search(indeed_params, config.max_jobs_per_source))
                advanced_tasks.append(indeed_task)
            
            # Configure LinkedIn search
            if self.linkedin_scraper:
                from linkedin_scraper import LinkedInSearchParams
                linkedin_params = LinkedInSearchParams(
                    keywords=" ".join(config.keywords[:3]),
                    location=config.locations[0] if config.locations else "Remote",
                    experience_level="mid_senior",
                    job_type="full_time",
                    date_posted="week"
                )
                linkedin_task = asyncio.create_task(self._run_linkedin_search(linkedin_params, config.max_jobs_per_source))
                advanced_tasks.append(linkedin_task)
                
        except Exception as e:
            logger.error(f"Failed to configure advanced scrapers: {e}")
        
        return advanced_tasks
    
    async def _run_indeed_search(self, params, max_jobs: int) -> List[JobOpportunity]:
        """Run Indeed search in async context"""
        try:
            # Run Indeed scraper in thread pool since it's not async
            loop = asyncio.get_event_loop()
            jobs_data = await loop.run_in_executor(
                None, 
                self.indeed_scraper.search_jobs, 
                params, 
                max_jobs
            )
            
            # Convert to JobOpportunity objects
            jobs = []
            for job_data in jobs_data:
                job = JobOpportunity(
                    title=job_data.get('title', ''),
                    company=job_data.get('company', ''),
                    location=job_data.get('location', ''),
                    salary_range=job_data.get('salary_range'),
                    job_type=job_data.get('job_type', 'full-time'),
                    source='indeed',
                    discovered_at=job_data.get('discovered_at', datetime.now().isoformat()),
                    url=job_data.get('url', ''),
                    job_id=self._generate_job_id(job_data.get('title', ''), job_data.get('company', ''), 'indeed'),
                    description=job_data.get('description', ''),
                    requirements=job_data.get('requirements', []),
                    technologies=job_data.get('technologies', [])
                )
                jobs.append(job)
            
            logger.info(f"Indeed scraper returned {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Indeed search failed: {e}")
            return []
    
    async def _run_linkedin_search(self, params, max_jobs: int) -> List[JobOpportunity]:
        """Run LinkedIn search in async context"""
        try:
            # Run LinkedIn scraper in thread pool since it's not async
            loop = asyncio.get_event_loop()
            jobs_data = await loop.run_in_executor(
                None, 
                self.linkedin_scraper.discover_opportunities, 
                params, 
                max_jobs
            )
            
            # Convert to JobOpportunity objects
            jobs = []
            for job_data in jobs_data:
                job = JobOpportunity(
                    title=job_data.get('title', ''),
                    company=job_data.get('company', ''),
                    location=job_data.get('location', ''),
                    salary_range=job_data.get('salary_range'),
                    job_type=job_data.get('job_type', 'full-time'),
                    source='linkedin',
                    discovered_at=job_data.get('discovered_at', datetime.now().isoformat()),
                    url=job_data.get('url', ''),
                    job_id=self._generate_job_id(job_data.get('title', ''), job_data.get('company', ''), 'linkedin'),
                    description=job_data.get('description', ''),
                    requirements=job_data.get('requirements', []),
                    technologies=job_data.get('technologies', [])
                )
                jobs.append(job)
            
            logger.info(f"LinkedIn scraper returned {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"LinkedIn search failed: {e}")
            return []
    
    def _generate_job_id(self, title: str, company: str, source: str) -> str:
        """Generate unique job ID"""
        unique_string = f"{title.lower()}_{company.lower()}_{source}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def _deduplicate_jobs(self, jobs: List[JobOpportunity]) -> List[JobOpportunity]:
        """Remove duplicate jobs based on title, company, and similarity"""
        seen_jobs = {}
        unique_jobs = []
        
        for job in jobs:
            # Create a similarity key
            key = f"{job.title.lower().strip()}_{job.company.lower().strip()}"
            
            if key not in seen_jobs:
                seen_jobs[key] = job
                unique_jobs.append(job)
            else:
                # Keep the job from the higher-priority source
                existing_job = seen_jobs[key]
                source_priority = {'linkedin': 3, 'indeed': 2, 'company': 1, 'hn_jobs': 1}
                
                if source_priority.get(job.source, 0) > source_priority.get(existing_job.source, 0):
                    # Replace with higher priority source
                    unique_jobs.remove(existing_job)
                    unique_jobs.append(job)
                    seen_jobs[key] = job
        
        logger.info(f"Deduplicated {len(jobs)} jobs to {len(unique_jobs)} unique jobs")
        return unique_jobs
    
    def get_discovered_jobs(self, limit: int = 50) -> List[JobOpportunity]:
        """Get recently discovered jobs"""
        return self.database.get_jobs_by_status('discovered', limit)
    
    def get_top_opportunities(self, limit: int = 20) -> List[JobOpportunity]:
        """Get top-ranked job opportunities"""
        return self.database.get_top_opportunities(limit)
    
    async def continuous_discovery(self, interval_hours: int = 4):
        """Run continuous job discovery"""
        logger.info(f"Starting continuous job discovery (every {interval_hours} hours)")
        
        while True:
            try:
                await self.discover_jobs()
                logger.info(f"Discovery cycle complete. Sleeping for {interval_hours} hours...")
                await asyncio.sleep(interval_hours * 3600)
            except Exception as e:
                logger.error(f"Discovery cycle failed: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry

# CLI Interface for testing
async def main():
    """Test the job discovery engine"""
    print("AI Job Hunt Commander - Job Discovery Engine Test")
    print("=" * 60)
    
    engine = JobDiscoveryEngine()
    
    print("Starting job discovery...")
    jobs = await engine.discover_jobs()
    
    print(f"\nDiscovered {len(jobs)} jobs:")
    print("-" * 40)
    
    for job in jobs:
        print(f"• {job.title} at {job.company}")
        print(f"  Location: {job.location}")
        print(f"  Source: {job.source}")
        print(f"  Technologies: {', '.join(job.technologies[:3])}")
        print()
    
    print("Job discovery test complete!")

if __name__ == "__main__":
    asyncio.run(main())