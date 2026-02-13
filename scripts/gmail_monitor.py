#!/usr/bin/env python3
"""Gmail Monitor - Check and categorize unread emails"""

import os
import json
import base64
import re
from datetime import datetime, timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Gmail API endpoints
GMAIL_API_BASE = "https://www.googleapis.com/gmail/v1/users/me"
TOKEN_URL = "https://oauth2.googleapis.com/token"

def load_credentials():
    """Load Google OAuth credentials from environment or credentials file."""
    # Try environment variables first
    client_id = os.getenv('GOOGLE_CLIENT_ID', '')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
    refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN', '')
    
    # If not in env, try credentials file
    if not all([client_id, client_secret, refresh_token]):
        creds_paths = ["../credentials/google-workspace.md", "credentials/google-workspace.md"]
        for creds_path in creds_paths:
            if os.path.exists(creds_path):
                with open(creds_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('client_id:'):
                            client_id = line.split(':', 1)[1].strip()
                        elif line.startswith('client_secret:'):
                            client_secret = line.split(':', 1)[1].strip()
                        elif line.startswith('refresh_token:'):
                            refresh_token = line.split(':', 1)[1].strip()
                break
    
    return client_id, client_secret, refresh_token

def refresh_access_token():
    """Refresh OAuth access token using refresh token"""
    client_id, client_secret, refresh_token = load_credentials()
    
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Google credentials not found. Set environment variables or add to credentials file.")
    
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    req = Request(TOKEN_URL, data=urlencode(data).encode())
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    
    try:
        with urlopen(req) as response:
            return json.loads(response.read())["access_token"]
    except HTTPError as e:
        raise Exception(f"Token refresh failed: {e.read().decode()}")

def get_unread_emails(access_token, minutes=30):
    """Get unread emails from last N minutes"""
    time_ago = (datetime.utcnow() - timedelta(minutes=minutes)).strftime('%Y/%m/%d %H:%M:%S')
    query = f"is:unread after:{time_ago}"
    
    url = f"{GMAIL_API_BASE}/messages?q={urlencode({'q': query})}"
    req = Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    
    try:
        with urlopen(req) as response:
            return json.loads(response.read())
    except HTTPError as e:
        raise Exception(f"Failed to fetch emails: {e.read().decode()}")

def get_email_details(access_token, msg_id):
    """Get full email details"""
    url = f"{GMAIL_API_BASE}/messages/{msg_id}"
    req = Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    
    try:
        with urlopen(req) as response:
            return json.loads(response.read())
    except HTTPError as e:
        raise Exception(f"Failed to fetch message {msg_id}: {e.read().decode()}")

def extract_content(email_data):
    """Extract subject and body from email"""
    subject = ""
    body = ""
    
    headers = email_data.get("payload", {}).get("headers", [])
    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"]
        elif header["name"] == "From":
            sender = header["value"]
    
    # Extract body
    parts = email_data.get("payload", {}).get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            break
    
    return subject, body, sender

def categorize_email(subject, body):
    """Categorize email based on content"""
    content = (subject + " " + body).lower()
    
    # Check for job-related keywords
    job_keywords = ["job", "application", "hiring", "position", "career", "opportunity", "role"]
    urgent_keywords = ["urgent", "interview", "deadline", "offer", "rejection"]
    
    if any(kw in content for kw in urgent_keywords):
        return "URGENT"
    elif any(kw in content for kw in job_keywords):
        return "Jobs"
    else:
        return "Personal"

def main():
    """Main function"""
    try:
        access_token = refresh_access_token()
        
        # Get unread emails from last 30 minutes
        emails_data = get_unread_emails(access_token, minutes=30)
        messages = emails_data.get("messages", [])
        
        if not messages:
            print("No new unread emails in the last 30 minutes.")
            return
        
        print(f"Found {len(messages)} unread email(s):")
        
        for msg in messages:
            msg_id = msg["id"]
            email_data = get_email_details(access_token, msg_id)
            subject, body, sender = extract_content(email_data)
            category = categorize_email(subject, body)
            
            print(f"\n  [{category}] From: {sender}")
            print(f"  Subject: {subject}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
