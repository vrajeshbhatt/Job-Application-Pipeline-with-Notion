"""
MAYAI Job Application Pipeline - Main Orchestrator

This script orchestrates the entire job application pipeline:
1. Search for jobs using Brave Search API
2. Score and filter matches (80%+ threshold)
3. Generate tailored resumes and cover letters
4. Upload to Notion database (optional)
5. Send notifications

Usage:
    python pipeline.py --search --generate --notify

Author: Vrajesh Bhatt
Date: February 2026
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Import pipeline modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from job_search import search_brave_jobs
    from resume_generator import generate_application_package
    from notion_sync import sync_to_notion
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required scripts are in the scripts/ folder")
    sys.exit(1)


class JobPipeline:
    """Main pipeline orchestrator for job application automation."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize pipeline with configuration."""
        self.config = self._load_config(config_path)
        self.results = {
            "jobs_found": [],
            "jobs_scored": [],
            "applications_generated": [],
            "errors": []
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        default_config = {
            "search_terms": [
                "entry level Data Analyst jobs Canada",
                "junior Data Analyst Halifax Nova Scotia",
                "Data Analyst 1-2 years experience Toronto"
            ],
            "location_priority": ["Halifax, NS", "Toronto, ON", "Remote, Canada"],
            "match_threshold": 80,
            "max_jobs": 50,
            "output_dir": "applications",
            "templates_dir": "templates"
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def search_jobs(self) -> List[Dict]:
        """
        Search for jobs using Brave Search API.
        
        Returns:
            List of job dictionaries with title, company, url, description
        """
        print("🔍 Searching for jobs...")
        
        jobs = []
        for term in self.config["search_terms"]:
            try:
                results = search_brave_jobs(term, count=10)
                jobs.extend(results)
                print(f"  Found {len(results)} jobs for: {term}")
            except Exception as e:
                self.results["errors"].append(f"Search error for '{term}': {e}")
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_jobs = []
        for job in jobs:
            if job['url'] not in seen_urls:
                seen_urls.add(job['url'])
                unique_jobs.append(job)
        
        self.results["jobs_found"] = unique_jobs[:self.config["max_jobs"]]
        print(f"✅ Total unique jobs found: {len(self.results['jobs_found'])}")
        return self.results["jobs_found"]
    
    def score_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Score jobs based on relevance to candidate profile.
        
        Scoring weights:
        - Location: 40%
        - Skills match: 30%
        - Company: 20%
        - Salary/Other: 10%
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            List of jobs with match_score added
        """
        print("📊 Scoring job matches...")
        
        scored_jobs = []
        for job in jobs:
            score = self._calculate_match_score(job)
            job['match_score'] = score
            scored_jobs.append(job)
        
        # Sort by score descending
        scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Filter by threshold
        filtered = [j for j in scored_jobs if j['match_score'] >= self.config['match_threshold']]
        
        self.results["jobs_scored"] = filtered
        print(f"✅ Jobs above {self.config['match_threshold']}% threshold: {len(filtered)}")
        return filtered
    
    def _calculate_match_score(self, job: Dict) -> int:
        """
        Calculate match score for a single job.
        
        Args:
            job: Job dictionary with title, description, location
            
        Returns:
            Match score (0-100)
        """
        score = 0
        content = f"{job.get('title', '')} {job.get('description', '')}".lower()
        location = job.get('location', '').lower()
        
        # Location scoring (40%)
        location_score = 0
        if 'halifax' in location or 'nova scotia' in location:
            location_score = 40  # Top priority
        elif 'toronto' in location or 'ontario' in location:
            location_score = 30  # Secondary
        elif 'remote' in location or 'canada' in location:
            location_score = 25
        
        # Skills scoring (30%)
        skills_score = 0
        skills_keywords = ['python', 'sql', 'power bi', 'data analysis', 'excel']
        for skill in skills_keywords:
            if skill in content:
                skills_score += 6  # Max 30
        skills_score = min(30, skills_score)
        
        # Experience level (20%)
        experience_score = 0
        if any(term in content for term in ['entry level', 'junior', '1-2 years', 'recent grad']):
            experience_score = 20
        elif '0-2 years' in content or 'new grad' in content:
            experience_score = 18
        
        # Other factors (10%)
        other_score = 0
        if 'data analyst' in job.get('title', '').lower():
            other_score += 5
        if 'full-time' in content or 'permanent' in content:
            other_score += 5
        
        total_score = location_score + skills_score + experience_score + other_score
        return min(100, total_score)
    
    def generate_applications(self, jobs: List[Dict]) -> List[str]:
        """
        Generate tailored resume and cover letter for each job.
        
        Args:
            jobs: List of scored job dictionaries
            
        Returns:
            List of paths to generated application packages
        """
        print("📄 Generating application packages...")
        
        generated = []
        for i, job in enumerate(jobs, 1):
            try:
                print(f"  [{i}/{len(jobs)}] {job.get('company', 'Unknown')} - {job.get('title', 'Unknown')[:50]}...")
                
                package_path = generate_application_package(
                    job=job,
                    template_dir=self.config['templates_dir'],
                    output_dir=self.config['output_dir']
                )
                generated.append(package_path)
                
            except Exception as e:
                self.results["errors"].append(f"Generation error for {job.get('title', 'Unknown')}: {e}")
        
        self.results["applications_generated"] = generated
        print(f"✅ Generated {len(generated)} application packages")
        return generated
    
    def sync_to_notion(self, jobs: List[Dict]) -> bool:
        """
        Sync job data to Notion database.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            True if successful, False otherwise
        """
        print("📓 Syncing to Notion...")
        
        try:
            success = sync_to_notion(jobs)
            if success:
                print("✅ Notion sync complete")
            return success
        except Exception as e:
            self.results["errors"].append(f"Notion sync error: {e}")
            print(f"❌ Notion sync failed: {e}")
            return False
    
    def run(self, search: bool = True, score: bool = True, 
            generate: bool = True, sync: bool = False) -> Dict:
        """
        Run the complete pipeline.
        
        Args:
            search: Whether to search for jobs
            score: Whether to score matches
            generate: Whether to generate applications
            sync: Whether to sync to Notion
            
        Returns:
            Results dictionary
        """
        print("=" * 60)
        print("🚀 MAYAI Job Application Pipeline")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # Step 1: Search
            if search:
                jobs = self.search_jobs()
                if not jobs:
                    print("❌ No jobs found. Stopping pipeline.")
                    return self.results
            else:
                jobs = self.results.get("jobs_found", [])
            
            # Step 2: Score
            if score and jobs:
                jobs = self.score_jobs(jobs)
                if not jobs:
                    print("❌ No jobs above threshold. Stopping pipeline.")
                    return self.results
            
            # Step 3: Generate
            if generate and jobs:
                self.generate_applications(jobs)
            
            # Step 4: Sync to Notion
            if sync and jobs:
                self.sync_to_notion(jobs)
            
        except Exception as e:
            self.results["errors"].append(f"Pipeline error: {e}")
            print(f"❌ Pipeline error: {e}")
        
        # Print summary
        print("=" * 60)
        print("📊 PIPELINE SUMMARY")
        print("=" * 60)
        print(f"Jobs found: {len(self.results['jobs_found'])}")
        print(f"Jobs above threshold: {len(self.results['jobs_scored'])}")
        print(f"Applications generated: {len(self.results['applications_generated'])}")
        print(f"Errors: {len(self.results['errors'])}")
        
        if self.results['errors']:
            print("\n⚠️  Errors encountered:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("=" * 60)
        return self.results


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="MAYAI Job Application Pipeline"
    )
    parser.add_argument(
        "--config", "-c",
        default="config.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--search", "-s",
        action="store_true",
        help="Search for jobs"
    )
    parser.add_argument(
        "--score", "-r",
        action="store_true",
        help="Score job matches"
    )
    parser.add_argument(
        "--generate", "-g",
        action="store_true",
        help="Generate application packages"
    )
    parser.add_argument(
        "--sync", "-n",
        action="store_true",
        help="Sync to Notion"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run complete pipeline (search, score, generate)"
    )
    
    args = parser.parse_args()
    
    # If --all is specified, enable all steps
    if args.all:
        args.search = args.score = args.generate = True
    
    # If no specific flags, run everything
    if not any([args.search, args.score, args.generate, args.sync]):
        args.search = args.score = args.generate = True
    
    # Initialize and run pipeline
    pipeline = JobPipeline(config_path=args.config)
    results = pipeline.run(
        search=args.search,
        score=args.score,
        generate=args.generate,
        sync=args.sync
    )
    
    # Save results to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"pipeline_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {results_file}")


if __name__ == "__main__":
    main()
