# chukanchi

## Setup

1. Copy the environment variables template:
   ```bash
   cp .env.example .env
   ```

2. Fill in your actual credentials in the `.env` file or set them as environment variables:
   ```bash
   export GOOGLE_OAUTH_CLIENT_ID="your-google-oauth-client-id"
   export AWS_ACCESS_KEY_ID="your-aws-access-key-id"
   export AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
   ```

## Security

This application follows security best practices:
- No hardcoded credentials in source code
- All sensitive configuration is loaded from environment variables
- Security tests ensure credentials are not accidentally committed

## Testing

Run the security tests to ensure no credentials are hardcoded:
```bash
python -m unittest tests.test_security -v
```
