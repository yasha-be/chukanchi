import os

try:
    from django.conf import settings
except ImportError:
    settings = None

# Configuration for OAuth and AWS credentials
# These should be set as environment variables or in Django settings
GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

# Validate that required credentials are configured
if not GOOGLE_OAUTH_CLIENT_ID:
    raise ValueError("GOOGLE_OAUTH_CLIENT_ID environment variable is required")

if not AWS_ACCESS_KEY_ID:
    raise ValueError("AWS_ACCESS_KEY_ID environment variable is required")

if not AWS_SECRET_ACCESS_KEY:
    raise ValueError("AWS_SECRET_ACCESS_KEY environment variable is required")
