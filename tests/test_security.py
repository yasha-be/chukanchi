import unittest
import os
import re
from unittest.mock import patch
import sys
sys.path.append('/workspace')

from chukanchi_be import AuthConfig, auth_config


class TestSecurityFix(unittest.TestCase):
    """Test cases to verify that hardcoded credentials have been removed"""
    
    def test_no_hardcoded_google_oauth_client_id(self):
        """Test that Google OAuth client ID is not hardcoded in the file"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for the specific pattern that was flagged by SAST
        google_oauth_pattern = r'\d+-[a-zA-Z0-9]+\.apps\.googleusercontent\.com'
        matches = re.findall(google_oauth_pattern, content)
        
        self.assertEqual(len(matches), 0, 
                        f"Found hardcoded Google OAuth client ID patterns: {matches}")
    
    def test_no_hardcoded_aws_credentials(self):
        """Test that AWS credentials are not hardcoded in the file"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for AWS Access Key ID pattern
        aws_key_pattern = r'AKIA[0-9A-Z]{16}'
        aws_matches = re.findall(aws_key_pattern, content)
        
        self.assertEqual(len(aws_matches), 0, 
                        f"Found hardcoded AWS Access Key IDs: {aws_matches}")
        
        # Check for AWS Secret Access Key pattern (base64-like strings)
        secret_pattern = r'[A-Za-z0-9/+=]{40}'
        # Only check for patterns that look like AWS secrets (not our code)
        lines = content.split('\n')
        for line in lines:
            if 'wJalrXUtnFEMI' in line or 'bPxRfiCYEXAMPLE' in line:
                self.fail(f"Found hardcoded AWS secret in line: {line}")
    
    @patch.dict(os.environ, {'GOOGLE_OAUTH_CLIENT_ID': 'test-client-id'})
    def test_google_oauth_client_id_from_env(self):
        """Test that Google OAuth client ID is read from environment variables"""
        config = AuthConfig()
        self.assertEqual(config.google_oauth_client_id, 'test-client-id')
    
    @patch.dict(os.environ, {'AWS_ACCESS_KEY_ID': 'test-access-key'})
    def test_aws_access_key_from_env(self):
        """Test that AWS access key is read from environment variables"""
        config = AuthConfig()
        self.assertEqual(config.aws_access_key_id, 'test-access-key')
    
    @patch.dict(os.environ, {'AWS_SECRET_ACCESS_KEY': 'test-secret-key'})
    def test_aws_secret_key_from_env(self):
        """Test that AWS secret key is read from environment variables"""
        config = AuthConfig()
        self.assertEqual(config.aws_secret_access_key, 'test-secret-key')
    
    def test_empty_credentials_when_no_env_vars(self):
        """Test that credentials are empty when environment variables are not set"""
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            config = AuthConfig()
            self.assertEqual(config.google_oauth_client_id, '')
            self.assertEqual(config.aws_access_key_id, '')
            self.assertEqual(config.aws_secret_access_key, '')
    
    def test_auth_config_instance_exists(self):
        """Test that auth_config instance is properly created"""
        self.assertIsInstance(auth_config, AuthConfig)


if __name__ == '__main__':
    unittest.main()
