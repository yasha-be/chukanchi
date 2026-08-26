import os

def get_google_oauth_config():
    """Get Google OAuth configuration from environment variables."""
    google_oauth_client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
    if not google_oauth_client_id:
        raise ValueError("GOOGLE_OAUTH_CLIENT_ID environment variable is required")
    return google_oauth_client_id

def get_aws_credentials():
    """Get AWS credentials from environment variables."""
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', '')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required")
    
    return {
        'access_key_id': aws_access_key_id,
        'secret_access_key': aws_secret_access_key
    }
