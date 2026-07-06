import os

# Google OAuth configuration
GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')

# AWS configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

# Configuration validation
def validate_credentials():
    """Validate that required credentials are configured"""
    if not GOOGLE_OAUTH_CLIENT_ID:
        raise ValueError("GOOGLE_OAUTH_CLIENT_ID environment variable is required")
    
    if not AWS_ACCESS_KEY_ID:
        raise ValueError("AWS_ACCESS_KEY_ID environment variable is required")
    
    if not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS_SECRET_ACCESS_KEY environment variable is required")

# Example usage
def get_google_oauth_config():
    """Get Google OAuth configuration"""
    validate_credentials()
    return {
        'client_id': GOOGLE_OAUTH_CLIENT_ID,
    }

def get_aws_config():
    """Get AWS configuration"""
    validate_credentials()
    return {
        'access_key_id': AWS_ACCESS_KEY_ID,
        'secret_access_key': AWS_SECRET_ACCESS_KEY,
    }
