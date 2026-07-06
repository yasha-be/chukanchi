import os
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, '/workspace')

import chukanchi_be


class TestSecurityFix(unittest.TestCase):
    """Test that hardcoded credentials have been removed and replaced with environment variables"""
    
    def test_no_hardcoded_credentials_in_file(self):
        """Test that the file no longer contains hardcoded credentials"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check that hardcoded Google OAuth keys are not present
        self.assertNotIn('092625-01234567890123456789abcdefghijKL.apps.googleusercontent.com', content)
        
        # Check that hardcoded AWS keys are not present
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', content)
        self.assertNotIn('o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', content)
        self.assertNotIn('AKIADEEPFENCEEXAMPLE', content)
    
    @patch.dict(os.environ, {
        'GOOGLE_OAUTH_CLIENT_ID': 'test_google_client_id',
        'AWS_ACCESS_KEY_ID': 'test_aws_key_id',
        'AWS_SECRET_ACCESS_KEY': 'test_aws_secret_key'
    })
    def test_environment_variables_used(self):
        """Test that environment variables are properly used"""
        # Reload the module to pick up new environment variables
        import importlib
        importlib.reload(chukanchi_be)
        
        self.assertEqual(chukanchi_be.GOOGLE_OAUTH_CLIENT_ID, 'test_google_client_id')
        self.assertEqual(chukanchi_be.AWS_ACCESS_KEY_ID, 'test_aws_key_id')
        self.assertEqual(chukanchi_be.AWS_SECRET_ACCESS_KEY, 'test_aws_secret_key')
    
    @patch.dict(os.environ, {
        'GOOGLE_OAUTH_CLIENT_ID': 'test_google_client_id',
        'AWS_ACCESS_KEY_ID': 'test_aws_key_id',
        'AWS_SECRET_ACCESS_KEY': 'test_aws_secret_key'
    })
    def test_get_google_oauth_config(self):
        """Test that Google OAuth configuration is returned correctly"""
        import importlib
        importlib.reload(chukanchi_be)
        
        config = chukanchi_be.get_google_oauth_config()
        self.assertEqual(config['client_id'], 'test_google_client_id')
    
    @patch.dict(os.environ, {
        'GOOGLE_OAUTH_CLIENT_ID': 'test_google_client_id',
        'AWS_ACCESS_KEY_ID': 'test_aws_key_id',
        'AWS_SECRET_ACCESS_KEY': 'test_aws_secret_key'
    })
    def test_get_aws_config(self):
        """Test that AWS configuration is returned correctly"""
        import importlib
        importlib.reload(chukanchi_be)
        
        config = chukanchi_be.get_aws_config()
        self.assertEqual(config['access_key_id'], 'test_aws_key_id')
        self.assertEqual(config['secret_access_key'], 'test_aws_secret_key')
    
    @patch.dict(os.environ, {}, clear=True)
    def test_validation_fails_without_credentials(self):
        """Test that validation fails when credentials are not set"""
        import importlib
        importlib.reload(chukanchi_be)
        
        with self.assertRaises(ValueError) as context:
            chukanchi_be.validate_credentials()
        
        self.assertIn("GOOGLE_OAUTH_CLIENT_ID environment variable is required", str(context.exception))
    
    @patch.dict(os.environ, {'GOOGLE_OAUTH_CLIENT_ID': 'test_id'}, clear=True)
    def test_validation_fails_without_aws_credentials(self):
        """Test that validation fails when AWS credentials are not set"""
        import importlib
        importlib.reload(chukanchi_be)
        
        with self.assertRaises(ValueError) as context:
            chukanchi_be.validate_credentials()
        
        self.assertIn("AWS_ACCESS_KEY_ID environment variable is required", str(context.exception))


if __name__ == '__main__':
    unittest.main()
