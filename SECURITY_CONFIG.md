# Security Configuration

## Overview

This repository has been updated to remove hardcoded credentials and implement secure credential management using environment variables.

## Required Environment Variables

The following environment variables must be set before running the application:

### Google OAuth Configuration
- `GOOGLE_OAUTH_CLIENT_ID`: Your Google OAuth 2.0 client ID

### AWS Configuration
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key

## Setting Environment Variables

### Linux/macOS
```bash
export GOOGLE_OAUTH_CLIENT_ID="your-google-oauth-client-id"
export AWS_ACCESS_KEY_ID="your-aws-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
```

### Windows
```cmd
set GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
set AWS_ACCESS_KEY_ID=your-aws-access-key-id
set AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
```

### Docker
```dockerfile
ENV GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
ENV AWS_ACCESS_KEY_ID=your-aws-access-key-id
ENV AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
```

## Security Best Practices

1. **Never commit credentials to version control**
2. **Use environment variables or secure credential management systems**
3. **Rotate credentials regularly**
4. **Use least privilege access principles**
5. **Monitor credential usage**

## Validation

The application includes built-in validation to ensure all required credentials are configured before use. If any required environment variable is missing, the application will raise a `ValueError` with a descriptive message.

## Testing

Run the security tests to verify the configuration:

```bash
python -m unittest tests.test_security_fix -v
```

All tests should pass, confirming that:
- No hardcoded credentials remain in the codebase
- Environment variables are properly used
- Validation works correctly
- Configuration functions return expected values
