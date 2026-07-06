import os

# Google OAuth configuration - use environment variables for security
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'your-google-oauth-client-id')

# AWS configuration - use environment variables for security
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'your-aws-access-key-id')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'your-aws-secret-access-key')

# Configuration example for CSV format
# Access key ID,Secret access key
# Use environment variables: AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

# Configuration examples - all credentials should be loaded from environment variables
# AccesskeyID => Use AWS_ACCESS_KEY_ID environment variable
# SecretAccessKey => Use AWS_SECRET_ACCESS_KEY environment variable
