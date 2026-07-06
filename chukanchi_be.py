import os

class SecurityConfig:
    """
    Secure configuration class for handling sensitive credentials.
    All credentials should be stored as environment variables or in secure configuration files.
    """
    
    @staticmethod
    def get_google_oauth_client_id():
        """
        Get Google OAuth client ID from environment variables.
        Set GOOGLE_OAUTH_CLIENT_ID environment variable.
        """
        return os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
    
    @staticmethod
    def get_aws_access_key_id():
        """
        Get AWS Access Key ID from environment variables.
        Set AWS_ACCESS_KEY_ID environment variable.
        """
        return os.environ.get('AWS_ACCESS_KEY_ID', '')
    
    @staticmethod
    def get_aws_secret_access_key():
        """
        Get AWS Secret Access Key from environment variables.
        Set AWS_SECRET_ACCESS_KEY environment variable.
        """
        return os.environ.get('AWS_SECRET_ACCESS_KEY', '')

def validate_credentials():
    """
    Validate that all required credentials are properly configured.
    Returns True if all credentials are available, False otherwise.
    """
    config = SecurityConfig()
    
    google_client_id = config.get_google_oauth_client_id()
    aws_access_key = config.get_aws_access_key_id()
    aws_secret_key = config.get_aws_secret_access_key()
    
    if not google_client_id:
        print("Warning: GOOGLE_OAUTH_CLIENT_ID environment variable not set")
        return False
    
    if not aws_access_key:
        print("Warning: AWS_ACCESS_KEY_ID environment variable not set")
        return False
    
    if not aws_secret_key:
        print("Warning: AWS_SECRET_ACCESS_KEY environment variable not set")
        return False
    
    return True
