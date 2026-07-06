import os

class AuthConfig:
    """Configuration class for authentication credentials"""
    
    @property
    def google_oauth_client_id(self):
        """Get Google OAuth client ID from environment variables"""
        return os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
    
    @property
    def aws_access_key_id(self):
        """Get AWS Access Key ID from environment variables"""
        return os.getenv('AWS_ACCESS_KEY_ID', '')
    
    @property
    def aws_secret_access_key(self):
        """Get AWS Secret Access Key from environment variables"""
        return os.getenv('AWS_SECRET_ACCESS_KEY', '')

auth_config = AuthConfig()
