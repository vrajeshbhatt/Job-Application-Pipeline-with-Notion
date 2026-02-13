"""
Notion Sync Module - Database Integration

Syncs job applications to Notion database for tracking.
"""

import os
import json
from typing import List, Dict
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None


def load_notion_token() -> str:
    """Load Notion API token from credentials file."""
    creds_path = "../credentials/notion.md"
    
    if not os.path.exists(creds_path):
        creds_path = "credentials/notion.md"
    
    if os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            content = f.read()
            # Look for token pattern
            if 'ntn_' in content:
                # Extract token
                for line in content.split('\n'):
                    if 'ntn_' in line:
                        # Extract token from line
                        parts = line.split('ntn_')
                        if len(parts) > 1:
                            return 'ntn_' + parts[1].split()[0].strip()
    
    # Fallback to environment variable
    return os.getenv('NOTION_TOKEN', '')


def load_database_id() -> str:
    """Load Notion database ID from config."""
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('notion_database_id', '')
    
    return os.getenv('NOTION_DATABASE_ID', '')


def sync_to_notion(jobs: List[Dict]) -> bool:
    """
    Sync job applications to Notion database.
    
    Args:
        jobs: List of job dictionaries
        
    Returns:
        True if successful, False otherwise
    """
    if not requests:
        print("  ⚠️  requests library not installed. Install with: pip install requests")
        return False
    
    token = load_notion_token()
    database_id = load_database_id()
    
    if not token:
        print("  ⚠️  Notion token not found. Add to credentials/notion.md")
        return False
    
    if not database_id:
        print("  ⚠️  Notion database ID not found. Add to config.json")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    success_count = 0
    
    for job in jobs:
        try:
            # Prepare page data
            page_data = {
                "parent": {"database_id": database_id},
                "properties": {
                    "Company": {
                        "title": [{"text": {"content": job.get("company", "Unknown")}}]
                    },
                    "Role": {
                        "rich_text": [{"text": {"content": job.get("title", "Unknown")}}]
                    },
                    "Location": {
                        "select": {"name": job.get("location", "Canada")}
                    },
                    "Match Score": {
                        "number": job.get("match_score", 0)
                    },
                    "Status": {
                        "select": {"name": "Not Applied"}
                    },
                    "Job URL": {
                        "url": job.get("url", "")
                    },
                    "Date Found": {
                        "date": {"start": datetime.now().isoformat()[:10]}
                    }
                }
            }
            
            # Create page in Notion
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=page_data
            )
            
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"  ⚠️  Failed to sync {job.get('company')}: {response.status_code}")
                
        except Exception as e:
            print(f"  ⚠️  Error syncing {job.get('company')}: {e}")
    
    print(f"  ✅ Synced {success_count}/{len(jobs)} jobs to Notion")
    return success_count > 0


def create_database_template():
    """Print instructions for creating Notion database."""
    print("""
    📋 Notion Database Setup Instructions:
    
    1. Create a new database in Notion (Table view)
    2. Add these properties:
       - Company (Title)
       - Role (Text)
       - Location (Select)
       - Match Score (Number)
       - Status (Select: Not Applied, Applied, Interview, Offer, Rejected)
       - Job URL (URL)
       - Date Found (Date)
       - Date Applied (Date)
       - Notes (Text)
    
    3. Get your database ID:
       - Open the database in Notion
       - Copy the URL: https://www.notion.so/workspace/[DATABASE_ID]?v=...
       - The DATABASE_ID is the long string after the last /
    
    4. Add to config.json:
       {
         "notion_database_id": "your-database-id-here"
       }
    
    5. Get your Notion integration token:
       - Go to https://www.notion.so/my-integrations
       - Create new integration
       - Copy the "Internal Integration Token"
       - Add to credentials/notion.md
    
    6. Share database with integration:
       - In Notion, click "Share" on your database
       - Add your integration
    """)


if __name__ == "__main__":
    # Test sync
    test_jobs = [
        {
            "title": "Data Analyst",
            "company": "Test Corp",
            "location": "Halifax, NS",
            "url": "https://example.com",
            "match_score": 85
        }
    ]
    
    print("Testing Notion sync...")
    success = sync_to_notion(test_jobs)
    
    if not success:
        create_database_template()
