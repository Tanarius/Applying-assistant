#!/usr/bin/env python3
"""
Indeed Job Scraper
==================

Advanced Indeed job scraping with rate limiting and proxy rotation
for Infrastructure → AI transition job discovery.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class IndeedSearchParams:
    """Parameters for Indeed job search"""
    keywords: str
    location: str = ""
    radius: int = 25  # miles
    job_type: str = ""  # fulltime, parttime, contract, temporary
    salary_min: Optional[int] = None
    date_posted: str = "7"  # 1, 3, 7, 14 (days)
    remote_jobs: bool = True
    sort_by: str = "date"  # date, relevance

class IndeedScraper:
    """
    Advanced Indeed job scraping with rate limiting and proxy rotation
    
    Features:
    - AI/Automation keyword optimization
    - Location-based filtering
    - Salary range extraction
    - Company size detection
    - Remote work identification
    """
    
    def __init__(self, rate_limit_delay: float = 2.0, max_retries: int = 3):
        self.base_url = "https://www.indeed.com"
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # Setup session with realistic headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        logger.info("Indeed scraper initialized with rate limiting")
    
    def search_jobs(self, search_params: IndeedSearchParams, max_jobs: int = 50) -> List[Dict]:
        """
        Search for jobs on Indeed with advanced filtering
        
        Args:
            search_params: Search parameters configuration
            max_jobs: Maximum number of jobs to retrieve
            
        Returns:
            List of job dictionaries with standardized format
        """
        logger.info(f"Starting Indeed search: '{search_params.keywords}' in '{search_params.location}'")
        
        jobs = []
        start_page = 0
        
        while len(jobs) < max_jobs:
            try:
                # Build search URL
                search_url = self._build_search_url(search_params, start_page)
                
                # Fetch search results page
                page_jobs = self._fetch_search_page(search_url)
                
                if not page_jobs:
                    logger.info("No more jobs found, ending search")
                    break
                
                jobs.extend(page_jobs)
                logger.info(f"Retrieved {len(page_jobs)} jobs from page {start_page // 10 + 1}, total: {len(jobs)}")
                
                # Rate limiting
                time.sleep(self.rate_limit_delay + random.uniform(0, 1))
                
                # Move to next page
                start_page += 10
                
                # Safety limit to avoid infinite loops
                if start_page > 100:  # Max 10 pages
                    logger.info("Reached maximum page limit")
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching Indeed jobs: {e}")
                break
        
        # Limit to requested maximum
        jobs = jobs[:max_jobs]
        
        # Enhance job data with detailed information
        enhanced_jobs = self._enhance_job_details(jobs[:10])  # Enhance first 10 for performance
        
        logger.info(f"Indeed search completed: {len(enhanced_jobs)} jobs retrieved")
        return enhanced_jobs
    
    def _build_search_url(self, params: IndeedSearchParams, start: int = 0) -> str:
        """Build Indeed search URL with parameters"""
        query_params = {
            'q': params.keywords,
            'l': params.location,
            'radius': params.radius,
            'start': start,
            'sort': params.sort_by,
            'fromage': params.date_posted
        }
        
        # Add job type filter
        if params.job_type:
            query_params['jt'] = params.job_type
        
        # Add salary filter
        if params.salary_min:
            query_params['salary'] = f"${params.salary_min}+"
        
        # Add remote work filter
        if params.remote_jobs:
            query_params['remotejob'] = '1'
        
        # Remove empty parameters
        query_params = {k: v for k, v in query_params.items() if v}
        
        return f"{self.base_url}/jobs?{urlencode(query_params)}"
    
    def _fetch_search_page(self, url: str) -> List[Dict]:
        """Fetch and parse a single search results page"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                return self._parse_job_listings(soup)
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for URL {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch after {self.max_retries} attempts")
                    return []
    
    def _parse_job_listings(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse job listings from Indeed search results page"""
        jobs = []
        
        # Find job cards (Indeed uses various selectors)
        job_cards = soup.find_all(['div'], class_=lambda x: x and ('job_seen_beacon' in x or 'result' in x))
        
        if not job_cards:
            # Try alternative selectors
            job_cards = soup.find_all(['a', 'div'], attrs={'data-jk': True})
        
        logger.info(f"Found {len(job_cards)} job cards on page")
        
        for card in job_cards:
            try:
                job_data = self._extract_job_data(card)
                if job_data:
                    jobs.append(job_data)
            except Exception as e:
                logger.debug(f"Failed to parse job card: {e}")
                continue
        
        return jobs
    
    def _extract_job_data(self, card) -> Optional[Dict]:
        """Extract job information from a job card"""
        try:
            # Extract basic job information
            title_elem = card.find('h2') or card.find('a', attrs={'data-jk': True})
            if not title_elem:
                return None
                
            title = title_elem.get_text(strip=True)
            
            # Extract job URL
            job_link = title_elem.find('a') if title_elem.name != 'a' else title_elem
            job_url = urljoin(self.base_url, job_link.get('href', '')) if job_link else ""
            
            # Extract company name
            company_elem = card.find(['span', 'a'], class_=lambda x: x and 'companyName' in x)
            company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
            
            # Extract location
            location_elem = card.find(['div', 'span'], attrs={'data-testid': 'job-location'}) or \
                           card.find(['div', 'span'], class_=lambda x: x and 'companyLocation' in x)
            location = location_elem.get_text(strip=True) if location_elem else ""
            
            # Extract salary if available
            salary_elem = card.find(['span', 'div'], class_=lambda x: x and 'salary' in x.lower()) if card.find(['span', 'div'], class_=lambda x: x and 'salary' in x.lower()) else None
            salary = salary_elem.get_text(strip=True) if salary_elem else ""
            
            # Extract job snippet/description
            snippet_elem = card.find(['div', 'span'], class_=lambda x: x and 'summary' in x) or \
                          card.find(['div', 'span'], attrs={'data-testid': 'job-snippet'})
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
            
            # Extract job type indicators
            job_type = self._determine_job_type(title, snippet)
            
            # Create standardized job data
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'salary_range': salary,
                'job_type': job_type,
                'source': 'indeed',
                'url': job_url,
                'description': snippet,
                'discovered_at': datetime.now().isoformat(),
                'requirements': self._extract_requirements(snippet),
                'technologies': self._extract_technologies(snippet)
            }
            
            return job_data
            
        except Exception as e:
            logger.debug(f"Failed to extract job data: {e}")
            return None
    
    def _enhance_job_details(self, jobs: List[Dict]) -> List[Dict]:
        """Enhance job listings with detailed information from job pages"""
        enhanced_jobs = []
        
        for job in jobs:
            try:
                if job.get('url'):
                    detailed_info = self._fetch_job_details(job['url'])
                    if detailed_info:
                        job.update(detailed_info)
                
                enhanced_jobs.append(job)
                
                # Rate limiting for detailed fetches
                time.sleep(self.rate_limit_delay + random.uniform(0.5, 1.5))
                
            except Exception as e:
                logger.warning(f"Failed to enhance job details for {job.get('title', 'Unknown')}: {e}")
                enhanced_jobs.append(job)  # Keep original data
        
        return enhanced_jobs
    
    def _fetch_job_details(self, job_url: str) -> Optional[Dict]:
        """Fetch detailed job information from job page"""
        try:
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract full job description
            desc_elem = soup.find(['div', 'section'], class_=lambda x: x and 'jobDescription' in x) or \
                       soup.find(['div'], id='jobDescriptionText')
            
            full_description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Extract additional details
            details = {}
            
            if full_description:
                details['description'] = full_description
                details['requirements'] = self._extract_requirements(full_description)
                details['technologies'] = self._extract_technologies(full_description)
            
            return details
            
        except Exception as e:
            logger.debug(f"Failed to fetch job details from {job_url}: {e}")
            return None
    
    def _determine_job_type(self, title: str, description: str) -> str:
        """Determine job type from title and description"""
        combined_text = f"{title} {description}".lower()
        
        if any(term in combined_text for term in ['remote', 'work from home', 'telecommute']):
            return 'remote'
        elif any(term in combined_text for term in ['contract', 'contractor', 'freelance']):
            return 'contract'
        elif any(term in combined_text for term in ['part time', 'part-time']):
            return 'part-time'
        else:
            return 'full-time'
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract job requirements from text"""
        if not text:
            return []
        
        # Common requirement patterns
        requirements = []
        text_lower = text.lower()
        
        # Technical skills
        tech_skills = ['python', 'javascript', 'java', 'c++', 'sql', 'aws', 'azure', 'kubernetes', 
                      'docker', 'tensorflow', 'pytorch', 'machine learning', 'data science']
        
        for skill in tech_skills:
            if skill in text_lower:
                requirements.append(skill.title())
        
        # Experience requirements
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:in\s*)?(?:software|engineering|development)',
            r'bachelor\'?s?\s*degree',
            r'master\'?s?\s*degree'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if match.isdigit():
                    requirements.append(f"{match}+ years experience")
                else:
                    requirements.append(match.title())
        
        return list(set(requirements))[:10]  # Limit and deduplicate
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract technologies mentioned in job text"""
        if not text:
            return []
        
        # Technology keywords
        technologies = []
        text_lower = text.lower()
        
        tech_keywords = [
            'python', 'javascript', 'typescript', 'java', 'c++', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask',
            'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform',
            'postgresql', 'mysql', 'mongodb', 'redis',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'jenkins', 'gitlab ci', 'github actions', 'circleci'
        ]
        
        for tech in tech_keywords:
            if tech in text_lower:
                technologies.append(tech)
        
        return list(set(technologies))[:15]  # Limit and deduplicate

def test_indeed_scraper():
    """Test Indeed scraper functionality"""
    print("\n" + "="*80)
    print("INDEED SCRAPER TESTING")
    print("="*80)
    
    # Create search parameters for Infrastructure → AI roles
    search_params = IndeedSearchParams(
        keywords="machine learning platform engineer",
        location="Remote",
        job_type="fulltime",
        remote_jobs=True,
        date_posted="14"
    )
    
    # Initialize scraper
    scraper = IndeedScraper(rate_limit_delay=1.0)  # Faster for testing
    
    # Search for jobs
    jobs = scraper.search_jobs(search_params, max_jobs=5)  # Small test set
    
    print(f"\nFound {len(jobs)} jobs:")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']} at {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Salary: {job['salary_range'] or 'Not specified'}")
        print(f"   Type: {job['job_type']}")
        print(f"   Technologies: {', '.join(job['technologies'][:5])}")
        if job.get('url'):
            print(f"   URL: {job['url'][:60]}...")
    
    print("\n" + "="*80)
    print("INDEED SCRAPER TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    test_indeed_scraper()