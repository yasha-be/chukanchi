import os

class CredentialsManager:
    """
    Secure credentials manager that retrieves sensitive information from environment variables
    instead of hardcoding them in the source code.
    """
    
    @staticmethod
    def get_google_oauth_key():
        """Get Google OAuth key from environment variable"""
        return os.getenv('GOOGLE_OAUTH_KEY', '')
    
    @staticmethod
    def get_aws_access_key_id():
        """Get AWS Access Key ID from environment variable"""
        return os.getenv('AWS_ACCESS_KEY_ID', '')
    
    @staticmethod
    def get_aws_secret_access_key():
        """Get AWS Secret Access Key from environment variable"""
        return os.getenv('AWS_SECRET_ACCESS_KEY', '')
    
    @staticmethod
    def validate_credentials():
        """Validate that all required credentials are available"""
        required_vars = ['GOOGLE_OAUTH_KEY', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
