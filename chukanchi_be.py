import os

# Configuration for OAuth and AWS credentials
# These should be set as environment variables for security
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')

# Example usage:
# export GOOGLE_OAUTH_CLIENT_ID="your-google-oauth-client-id"
# export AWS_ACCESS_KEY_ID="your-aws-access-key-id"
# export AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
