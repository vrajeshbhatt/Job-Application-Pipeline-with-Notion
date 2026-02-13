# LinkedIn OAuth 2.0 Configuration

## Overview
This setup enables MAYAI to access LinkedIn's official APIs for job search and posting.

## Prerequisites
1. LinkedIn Developer Account (https://developer.linkedin.com/)
2. LinkedIn App created in the Developer Portal
3. OAuth 2.0 credentials (Client ID and Client Secret)

## Required API Products
You need to apply for these products in your LinkedIn app:
- **Share on LinkedIn** (basic profile access)
- **Advertising API** (optional, for job posting)
- **Recruiter System Connect** (for job search - requires LinkedIn partnership)

⚠️ **Important:** LinkedIn's Job Search API requires a formal partnership application.
For now, we'll set up basic OAuth for profile access and prepare the infrastructure.

## Setup Steps

### Step 1: Create LinkedIn App
1. Go to https://developer.linkedin.com/
2. Click "Create App"
3. Fill in:
   - App Name: "MAYAI Job Assistant"
   - LinkedIn Page: (Your LinkedIn company page or personal profile)
   - App Logo: Upload MAYAI logo
   - Legal Agreement: Accept terms

### Step 2: Configure OAuth 2.0
1. In your app dashboard, go to "Auth" tab
2. Add Authorized Redirect URLs:
   - `http://localhost:8080/callback` (for local testing)
   - `https://mayai.local/callback` (for production)
3. Copy the **Client ID** and **Client Secret**

### Step 3: Request API Access
1. Go to "Products" tab
2. Request "Share on LinkedIn" (immediate approval)
3. Request "Sign In with LinkedIn using OpenID Connect" (immediate approval)
4. For job search, you'll need to contact LinkedIn Partnerships:
   - Email: partner@linkedin.com
   - Or apply at: https://developer.linkedin.com/partner-programs

### Step 4: Store Credentials
Add your credentials to `credentials/linkedin-oauth.md` (already created below)

## Scopes Needed
- `openid` - Basic profile info
- `profile` - Full profile access
- `email` - Email address
- `w_member_social` - Share posts (if needed)

## Rate Limits
- Basic API: 500 requests/day
- With partnership: Higher limits available

## Security Notes
- Never commit Client Secret to git
- Store refresh tokens securely
- Tokens expire every 60 days and must be refreshed
