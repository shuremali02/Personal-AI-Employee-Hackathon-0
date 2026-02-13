# Gmail API Setup Guide

## Prerequisites
- Google account with Gmail enabled
- Google Cloud Platform project
- Enabled Gmail API in Google Cloud Console

## Setup Steps

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing for the project (if required)

### 2. Enable Gmail API
1. In Google Cloud Console, go to APIs & Services > Library
2. Search for "Gmail API"
3. Click "Enable" for the Gmail API

### 3. Create OAuth 2.0 Credentials
1. Go to APIs & Services > Credentials
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Configure the OAuth consent screen
4. Download the credentials JSON file
5. Rename to `gmail-credentials.json`

### 4. Configure Application
1. Place `gmail-credentials.json` in the project root
2. Update `.env` file with:
   ```
   GMAIL_CLIENT_ID=your_client_id
   GMAIL_CLIENT_SECRET=your_client_secret
   GMAIL_REDIRECT_URI=http://localhost:8080/callback
   ```

### 5. Authorization Flow
The application will guide you through the OAuth flow to obtain access tokens.

## Required Scopes
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails
- `https://www.googleapis.com/auth/gmail.send` - Send emails

## Rate Limits
- 250 units per day
- 10 units per 100 seconds per user
