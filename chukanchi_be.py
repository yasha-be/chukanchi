import os

# Use environment variables for sensitive credentials
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'your-google-oauth-client-id')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'your-aws-access-key-id')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'your-aws-secret-access-key')

# Configuration class for managing credentials securely
class Config:
    def __init__(self):
        self.google_oauth_client_id = GOOGLE_OAUTH_CLIENT_ID
        self.aws_access_key_id = AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    
    def get_google_oauth_client_id(self):
        return self.google_oauth_client_id
    
    def get_aws_credentials(self):
        return {
            'access_key_id': self.aws_access_key_id,
            'secret_access_key': self.aws_secret_access_key
        }
