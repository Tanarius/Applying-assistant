#!/usr/bin/env python3
"""
Progress Tracker
================

Real-time progress tracking with visual indicators for AI application generation.
Shows detailed status updates, timing, and prevents user confusion about whether
the system is working or frozen.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class ProgressStage(Enum):
    """Stages of application generation"""
    INITIALIZING = "Initializing"
    COMPANY_RESEARCH = "Company Research"
    BUSINESS_ANALYSIS = "Business Analysis" 
    TECHNICAL_RESEARCH = "Technical Research"
    MARKET_ANALYSIS = "Market Analysis"
    POSITIONING_STRATEGY = "Positioning Strategy"
    COVER_LETTER_GENERATION = "Cover Letter Generation"
    EXECUTIVE_SUMMARY = "Executive Summary"
    INTERVIEW_PREP = "Interview Preparation" 
    SUCCESS_STRATEGY = "Success Strategy"
    FINALIZING = "Finalizing Package"
    COMPLETE = "Complete"

@dataclass
class ProgressUpdate:
    """Individual progress update"""
    timestamp: datetime
    stage: ProgressStage
    message: str
    progress_percent: float
    estimated_remaining: Optional[float] = None
    details: Optional[str] = None

class ProgressTracker:
    """
    Real-time progress tracking with visual feedback
    """
    
    def __init__(self, estimated_total_time: float = 90.0):
        """Initialize progress tracker"""
        self.start_time = datetime.now()
        self.estimated_total_time = estimated_total_time
        self.current_stage = ProgressStage.INITIALIZING
        self.progress_updates: List[ProgressUpdate] = []
        self.stage_timings: Dict[ProgressStage, float] = {}
        self.is_active = False
        self.spinner_thread = None
        self.last_update_time = time.time()
        
        # Stage timing estimates (seconds)
        self.stage_estimates = {
            ProgressStage.INITIALIZING: 2,
            ProgressStage.COMPANY_RESEARCH: 15,
            ProgressStage.BUSINESS_ANALYSIS: 10,
            ProgressStage.TECHNICAL_RESEARCH: 12,
            ProgressStage.MARKET_ANALYSIS: 8,
            ProgressStage.POSITIONING_STRATEGY: 8,
            ProgressStage.COVER_LETTER_GENERATION: 15,
            ProgressStage.EXECUTIVE_SUMMARY: 5,
            ProgressStage.INTERVIEW_PREP: 10,
            ProgressStage.SUCCESS_STRATEGY: 5,
            ProgressStage.FINALIZING: 3,
        }
    
    def start(self, total_stages: int = 11):
        """Start progress tracking"""
        self.is_active = True
        self.total_stages = total_stages
        print("\n" + "="*80)
        print("AI APPLICATION GENERATION - LIVE PROGRESS TRACKING")
        print("="*80)
        print(f"* Estimated time: {self.estimated_total_time:.0f} seconds")
        print(f"* Started at: {self.start_time.strftime('%H:%M:%S')}")
        print("* Real-time updates below (system is working, please wait)...")
        print("-" * 80)
        
        # Start background spinner
        self._start_activity_monitor()
    
    def update_stage(self, stage: ProgressStage, message: str, details: Optional[str] = None):
        """Update current stage with message"""
        if not self.is_active:
            return
            
        # Record timing for previous stage
        if self.current_stage != ProgressStage.INITIALIZING:
            elapsed = time.time() - self.last_update_time
            self.stage_timings[self.current_stage] = elapsed
        
        self.current_stage = stage
        self.last_update_time = time.time()
        
        # Calculate progress
        stage_index = list(ProgressStage).index(stage)
        progress_percent = (stage_index / len(ProgressStage)) * 100
        
        # Estimate remaining time
        elapsed_total = time.time() - self.start_time.timestamp()
        if progress_percent > 5:  # Avoid division by zero
            estimated_total = elapsed_total * (100 / progress_percent)
            estimated_remaining = max(0, estimated_total - elapsed_total)
        else:
            estimated_remaining = self.estimated_total_time - elapsed_total
        
        # Create update
        update = ProgressUpdate(
            timestamp=datetime.now(),
            stage=stage,
            message=message,
            progress_percent=progress_percent,
            estimated_remaining=estimated_remaining,
            details=details
        )
        
        self.progress_updates.append(update)
        self._display_update(update)
    
    def update_progress(self, message: str, details: Optional[str] = None):
        """Update progress within current stage"""
        if not self.is_active:
            return
            
        # Create mini-update for current stage
        elapsed_total = time.time() - self.start_time.timestamp()
        stage_index = list(ProgressStage).index(self.current_stage)
        progress_percent = (stage_index / len(ProgressStage)) * 100
        
        estimated_remaining = max(0, self.estimated_total_time - elapsed_total)
        
        update = ProgressUpdate(
            timestamp=datetime.now(),
            stage=self.current_stage,
            message=message,
            progress_percent=progress_percent,
            estimated_remaining=estimated_remaining,
            details=details
        )
        
        self._display_mini_update(update)
    
    def _display_update(self, update: ProgressUpdate):
        """Display major stage update"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Progress bar
        bar_length = 40
        filled_length = int(bar_length * update.progress_percent / 100)
        bar = "+" * filled_length + "-" * (bar_length - filled_length)
        
        print(f"\n[{bar}] {update.progress_percent:.1f}%")
        print(f"* STAGE: {update.stage.value}")
        print(f"* STATUS: {update.message}")
        if update.details:
            print(f"* DETAIL: {update.details}")
        print(f"* ELAPSED: {elapsed:.1f}s | REMAINING: ~{update.estimated_remaining:.0f}s")
        
        # Show estimated completion time
        completion_time = datetime.now() + timedelta(seconds=update.estimated_remaining or 0)
        print(f"* ETA: {completion_time.strftime('%H:%M:%S')}")
        print("-" * 60)
    
    def _display_mini_update(self, update: ProgressUpdate):
        """Display minor progress update"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        timestamp = update.timestamp.strftime('%H:%M:%S')
        print(f"  [{timestamp}] {update.message}")
        if update.details:
            print(f"             └─ {update.details}")
    
    def _start_activity_monitor(self):
        """Start background activity indicator"""
        def activity_spinner():
            spinner_chars = "|/-\\"
            i = 0
            last_activity = time.time()
            
            while self.is_active:
                current_time = time.time()
                
                # Show spinner if no recent updates
                if current_time - self.last_update_time > 3:
                    elapsed = current_time - self.start_time.timestamp()
                    print(f"\r  [{spinner_chars[i % len(spinner_chars)]}] Working... ({elapsed:.0f}s elapsed)", end='', flush=True)
                    i += 1
                
                time.sleep(0.5)
        
        self.spinner_thread = threading.Thread(target=activity_spinner, daemon=True)
        self.spinner_thread.start()
    
    def complete(self, success_message: str = "Application generation completed successfully!"):
        """Mark progress as complete"""
        self.is_active = False
        
        total_elapsed = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\r{' ' * 60}\r", end='')  # Clear spinner
        print("\n" + "="*80)
        print("*** AI APPLICATION GENERATION COMPLETED ***")
        print("="*80)
        print(f"* {success_message}")
        print(f"* Total time: {total_elapsed:.1f} seconds")
        print(f"* Completed at: {datetime.now().strftime('%H:%M:%S')}")
        
        # Show stage timing breakdown
        print(f"\n* STAGE TIMING BREAKDOWN:")
        total_tracked = 0
        for stage, timing in self.stage_timings.items():
            print(f"   {stage.value}: {timing:.1f}s")
            total_tracked += timing
        
        print(f"   Total tracked: {total_tracked:.1f}s")
        print("="*80)
    
    def error(self, error_message: str, details: Optional[str] = None):
        """Handle error state"""
        self.is_active = False
        
        total_elapsed = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\r{' ' * 60}\r", end='')  # Clear spinner
        print("\n" + "="*80)
        print("*** ERROR IN AI APPLICATION GENERATION ***")
        print("="*80)
        print(f"* ERROR: {error_message}")
        if details:
            print(f"* DETAILS: {details}")
        print(f"* Failed after: {total_elapsed:.1f} seconds")
        print(f"* Failed at stage: {self.current_stage.value}")
        print("="*80)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get progress summary"""
        total_elapsed = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'start_time': self.start_time.isoformat(),
            'total_elapsed': total_elapsed,
            'current_stage': self.current_stage.value,
            'progress_percent': (list(ProgressStage).index(self.current_stage) / len(ProgressStage)) * 100,
            'total_updates': len(self.progress_updates),
            'stage_timings': {stage.value: timing for stage, timing in self.stage_timings.items()},
            'is_active': self.is_active
        }

# Example usage and testing
if __name__ == "__main__":
    import random
    
    # Demo progress tracking
    tracker = ProgressTracker(estimated_total_time=60)
    tracker.start()
    
    stages = [
        (ProgressStage.COMPANY_RESEARCH, "Gathering company intelligence", "Analyzing business model and market position"),
        (ProgressStage.BUSINESS_ANALYSIS, "Analyzing business fundamentals", "Financial health and competitive landscape"),
        (ProgressStage.TECHNICAL_RESEARCH, "Researching technical challenges", "Infrastructure and technology stack analysis"),
        (ProgressStage.POSITIONING_STRATEGY, "Developing positioning strategy", "Career transition and value proposition"),
        (ProgressStage.COVER_LETTER_GENERATION, "Generating AI cover letter", "Personalized content based on research"),
        (ProgressStage.EXECUTIVE_SUMMARY, "Creating executive summary", "Strategic positioning summary"),
        (ProgressStage.INTERVIEW_PREP, "Preparing interview strategy", "Company-specific questions and focus areas"),
        (ProgressStage.SUCCESS_STRATEGY, "Developing success plan", "Application optimization recommendations"),
        (ProgressStage.FINALIZING, "Finalizing application package", "Quality assurance and formatting")
    ]
    
    for stage, message, details in stages:
        tracker.update_stage(stage, message, details)
        time.sleep(random.uniform(2, 8))  # Simulate variable timing
        
        # Simulate sub-progress
        for i in range(random.randint(1, 3)):
            tracker.update_progress(f"Processing step {i+1}...")
            time.sleep(random.uniform(1, 3))
    
    tracker.complete("Demo application generation completed!")