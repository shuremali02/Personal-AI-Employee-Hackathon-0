# Banking API Setup Guide

## Supported Banks
This framework supports integration with various banking APIs that provide transaction monitoring capabilities.

## Setup Steps

### 1. Obtain API Credentials
1. Contact your bank to request API access
2. Register your application if required
3. Obtain API key and secret
4. Understand rate limits and usage policies

### 2. Configuration
Update `.env` file with:
```
BANKING_API_BASE_URL=https://api.yourbank.com
BANKING_API_KEY=your_api_key
BANKING_API_SECRET=your_api_secret
BANKING_ACCOUNT_ID=your_account_id
BANKING_WEBHOOK_URL=https://yourdomain.com/webhook/banking
```

### 3. Security Considerations
- Use HTTPS for all API calls
- Implement proper authentication
- Store credentials securely
- Monitor API usage for anomalies

## Common Endpoints
- GET /accounts/{id}/transactions - Retrieve transactions
- GET /accounts/{id}/balance - Get account balance
- POST /accounts/{id}/notifications - Set up notifications

## Rate Limits
- Varies by institution (typically 1000-10000 requests/day)
