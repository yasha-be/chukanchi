# chukanchi

## Security Configuration

This application requires the following environment variables to be set for proper authentication:

### Required Environment Variables

- `GOOGLE_OAUTH_CLIENT_ID`: Your Google OAuth 2.0 client ID
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID  
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key

### Setup Instructions

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your actual credentials:
   ```bash
   GOOGLE_OAUTH_CLIENT_ID=your_actual_google_oauth_client_id
   AWS_ACCESS_KEY_ID=your_actual_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_actual_aws_secret_access_key
   ```

3. Load the environment variables before running the application:
   ```bash
   source .env
   python chukanchi_be.py
   ```

### Security Notes

- **Never commit actual credentials to version control**
- The `.env` file is ignored by git to prevent accidental commits
- All credentials are now loaded from environment variables instead of being hardcoded
- The application will raise an error if required credentials are missing

## Testing

Run the security tests to verify the configuration:

```bash
python -m unittest tests.test_security -v
```
