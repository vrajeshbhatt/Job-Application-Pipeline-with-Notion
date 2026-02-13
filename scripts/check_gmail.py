#!/usr/bin/env python3
"""Check Gmail for unread emails from last 30 minutes."""

import json
import re
from datetime import datetime, timedelta
import requests
import os

def load_credentials():
    """Load Google OAuth credentials from environment or credentials file."""
    # Try environment variables first
    client_id = os.getenv('GOOGLE_CLIENT_ID', '')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
    refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN', '')
    
    # If not in env, try credentials file
    if not all([client_id, client_secret, refresh_token]):
        creds_path = "../credentials/google-workspace.md"
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
    
    return client_id, client_secret, refresh_token

def get_access_token():
    """Refresh access token using refresh token."""
    client_id, client_secret, refresh_token = load_credentials()
    
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Google credentials not found. Set environment variables or add to credentials file.")
    
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def check_gmail():
    """Check Gmail for unread emails from last 30 minutes."""
    try:
        access_token = get_access_token()
        
        # Calculate time 30 minutes ago
        time_30_min_ago = (datetime.utcnow() - timedelta(minutes=30)).strftime('%Y/%m/%d %H:%M:%S')
        
        # Search for unread emails from last 30 minutes
        query = f"is:unread after:{time_30_min_ago}"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages?q={requests.utils.quote(query)}",
            headers=headers
        )
        
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            
            if not messages:
                print("No new unread emails in the last 30 minutes.")
                return []
            
            print(f"Found {len(messages)} unread email(s) from last 30 minutes:")
            
            for msg in messages:
                msg_id = msg['id']
                msg_response = requests.get(
                    f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
                    headers=headers
                )
                
                if msg_response.status_code == 200:
                    msg_data = msg_response.json()
                    headers_list = msg_data.get('payload', {}).get('headers', [])
                    
                    subject = ""
                    sender = ""
                    
                    for header in headers_list:
                        if header['name'] == 'Subject':
                            subject = header['value']
                        elif header['name'] == 'From':
                            sender = header['value']
                    
                    print(f"  - From: {sender}")
                    print(f"    Subject: {subject}")
                    print()
            
            return messages
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error checking Gmail: {e}")
        return []

if __name__ == "__main__":
    check_gmail()
