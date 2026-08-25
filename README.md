# chukanchi

## Security Configuration

This application uses environment variables to securely manage sensitive credentials. **Never commit hardcoded credentials to version control.**

### Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual credentials:
   ```bash
   GOOGLE_OAUTH_KEY=your_actual_google_oauth_key
   AWS_ACCESS_KEY_ID=your_actual_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_actual_aws_secret_access_key
   ```

### Usage

Use the `CredentialsManager` class to securely access credentials:

```python
from chukanchi_be import CredentialsManager

# Get credentials
google_key = CredentialsManager.get_google_oauth_key()
aws_key_id = CredentialsManager.get_aws_access_key_id()
aws_secret = CredentialsManager.get_aws_secret_access_key()

# Validate all credentials are present
CredentialsManager.validate_credentials()
```

### Security Notes

- All sensitive credentials are now retrieved from environment variables
- The `.env` file is ignored by git to prevent accidental commits
- Use the provided `CredentialsManager` class for all credential access
- Validate credentials before using them in production
