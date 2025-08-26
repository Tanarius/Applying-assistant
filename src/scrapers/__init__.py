#!/usr/bin/env python3
"""
Job Scrapers Package
===================

Multi-source job scraping modules for the AI Job Hunt Commander.
Includes Indeed, LinkedIn, company website, and specialized scrapers.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

from .indeed_scraper import IndeedScraper, IndeedSearchParams
from .linkedin_scraper import LinkedInScraper, LinkedInSearchParams

__all__ = [
    'IndeedScraper',
    'IndeedSearchParams', 
    'LinkedInScraper',
    'LinkedInSearchParams'
]

__version__ = '2.0.0'