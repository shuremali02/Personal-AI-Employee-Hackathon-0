# WhatsApp Web Session Setup Guide

## Prerequisites
- WhatsApp account on mobile device
- Stable internet connection
- Chrome or Firefox browser

## Setup Steps

### 1. QR Code Authentication
1. The application will launch a browser instance
2. Navigate to web.whatsapp.com
3. Scan the QR code with your phone's camera
4. Session will be saved for future use

### 2. Session Persistence
- Sessions are stored in the `sessions/` directory
- Session cookies are saved for continued access
- Sessions expire periodically and need re-authentication

### 3. Configuration
Update `.env` file with:
```
WHATSAPP_HEADLESS_MODE=true
WHATSAPP_AUTO_RESTART=true
WHATSAPP_SESSION_TIMEOUT=3600
```

## Capabilities
- Read incoming messages
- Send automated responses
- Manage contacts
- Handle media files

## Limitations
- Requires phone to remain online
- WhatsApp may detect automation and restrict access
- Rate limits apply to message sending
