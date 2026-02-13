"""
Job Search Module - Brave Search API Integration

Searches for jobs using Brave Search API and returns structured results.
"""

import urllib.request
import json
import ssl
import os
from typing import List, Dict


def load_brave_api_key() -> str:
    """Load Brave Search API key from credentials file."""
    creds_path = "../credentials/brave-search.md"
    
    if not os.path.exists(creds_path):
        # Try alternative path
        creds_path = "credentials/brave-search.md"
    
    if os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            for line in f:
                if 'api key:' in line.lower() or 'token:' in line.lower():
                    return line.split(':', 1)[1].strip()
    
    # Fallback to environment variable
    return os.getenv('BRAVE_API_KEY', '')


def search_brave_jobs(query: str, count: int = 10, country: str = 'ca') -> List[Dict]:
    """
    Search for jobs using Brave Search API.
    
    Args:
        query: Search query (e.g., "Data Analyst jobs Halifax")
        count: Number of results to return (max 20)
        country: Country code for search (default: 'ca' for Canada)
        
    Returns:
        List of job dictionaries with title, url, description, source
    """
    api_key = load_brave_api_key()
    
    if not api_key:
        raise ValueError("Brave Search API key not found. Add to credentials/brave-search.md or set BRAVE_API_KEY env var.")
    
    headers = {
        'X-Subscription-Token': api_key,
        'Accept': 'application/json'
    }
    
    # Construct search URL
    encoded_query = urllib.parse.quote(query)
    url = f'https://api.search.brave.com/res/v1/web/search?q={encoded_query}&count={count}&country={country}'
    
    # Create SSL context
    ctx = ssl.create_default_context()
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            
            jobs = []
            for result in data.get('web', {}).get('results', []):
                job = {
                    'title': result.get('title', 'Unknown Title'),
                    'url': result.get('url', ''),
                    'description': result.get('description', '')[:500],
                    'source': extract_source(result.get('url', '')),
                    'location': extract_location(result.get('description', '')),
                    'company': extract_company(result.get('title', ''), result.get('url', ''))
                }
                jobs.append(job)
            
            return jobs
            
    except urllib.error.HTTPError as e:
        raise Exception(f"Brave Search API error: {e.code} - {e.reason}")
    except Exception as e:
        raise Exception(f"Search failed: {e}")


def extract_source(url: str) -> str:
    """Extract job board source from URL."""
    if 'indeed.com' in url:
        return 'Indeed'
    elif 'linkedin.com' in url:
        return 'LinkedIn'
    elif 'glassdoor.com' in url:
        return 'Glassdoor'
    elif 'ziprecruiter.com' in url:
        return 'ZipRecruiter'
    elif 'workopolis.com' in url:
        return 'Workopolis'
    elif 'jobbank.gc.ca' in url:
        return 'Job Bank Canada'
    else:
        return 'Other'


def extract_location(description: str) -> str:
    """Extract location from job description."""
    # Common Canadian cities/provinces
    locations = [
        'Toronto, ON', 'Vancouver, BC', 'Montreal, QC', 'Calgary, AB',
        'Halifax, NS', 'Ottawa, ON', 'Edmonton, AB', 'Winnipeg, MB',
        'Quebec City, QC', 'Victoria, BC', 'Saskatoon, SK', 'Regina, SK',
        'St. John\'s, NL', 'Fredericton, NB', 'Charlottetown, PEI',
        'Remote, Canada', 'Hybrid, Canada'
    ]
    
    desc_lower = description.lower()
    for location in locations:
        if location.split(',')[0].lower() in desc_lower:
            return location
    
    return 'Canada'


def extract_company(title: str, url: str) -> str:
    """Extract company name from title or URL."""
    # Try to extract from LinkedIn URL
    if 'linkedin.com/jobs/view' in url:
        parts = url.split('/')
        if len(parts) > 4:
            return parts[4].replace('-', ' ').title()
    
    # Try to extract from title (common pattern: "Job Title at Company")
    if ' at ' in title:
        return title.split(' at ')[-1].split('-')[0].strip()
    
    return 'Unknown Company'


if __name__ == "__main__":
    # Test search
    print("Testing Brave Search...")
    try:
        results = search_brave_jobs("Data Analyst Halifax", count=5)
        print(f"Found {len(results)} jobs:")
        for job in results[:3]:
            print(f"  - {job['title'][:60]}... ({job['source']})")
    except Exception as e:
        print(f"Error: {e}")
