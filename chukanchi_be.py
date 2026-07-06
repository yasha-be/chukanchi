import os

# Google OAuth configuration
GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', 'your-google-oauth-client-id')

# AWS configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'your-aws-access-key-id')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'your-aws-secret-access-key')

# Configuration examples (use environment variables in production)
# Google Oauth key: Set GOOGLE_OAUTH_CLIENT_ID environment variable
# AWS Access Key ID: Set AWS_ACCESS_KEY_ID environment variable
# AWS Secret Access Key: Set AWS_SECRET_ACCESS_KEY environment variable
