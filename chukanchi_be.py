import os

class Config:
    """Configuration class for secure credential management"""
    
    @staticmethod
    def get_google_oauth_key():
        """Get Google OAuth key from environment variables"""
        return os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
    
    @staticmethod
    def get_aws_access_key_id():
        """Get AWS Access Key ID from environment variables"""
        return os.environ.get('AWS_ACCESS_KEY_ID', '')
    
    @staticmethod
    def get_aws_secret_access_key():
        """Get AWS Secret Access Key from environment variables"""
        return os.environ.get('AWS_SECRET_ACCESS_KEY', '')

# Usage example:
# google_oauth_key = Config.get_google_oauth_key()
# aws_access_key_id = Config.get_aws_access_key_id()
# aws_secret_access_key = Config.get_aws_secret_access_key()
