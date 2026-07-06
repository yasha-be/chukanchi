import os
import sys
import unittest
from unittest.mock import patch

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chukanchi_be


class TestCredentialsConfiguration(unittest.TestCase):
    """Test that credentials are properly configured using environment variables"""

    def test_no_hardcoded_credentials_in_file(self):
        """Test that the source file doesn't contain hardcoded credentials"""
        with open('chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check that no hardcoded Google OAuth keys are present
        self.assertNotIn('092625-01234567890123456789abcdefghijKL.apps.googleusercontent.com', content)
        self.assertNotIn('625-01234567890123456789abcdefghijKL.apps.googleusercontent.com', content)
        
        # Check that no hardcoded AWS keys are present
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', content)
        self.assertNotIn('o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', content)
        self.assertNotIn('AKIADEEPFENCEEXAMPLE', content)

    @patch.dict(os.environ, {
        'GOOGLE_OAUTH_CLIENT_ID': 'test-google-client-id',
        'AWS_ACCESS_KEY_ID': 'test-aws-access-key',
        'AWS_SECRET_ACCESS_KEY': 'test-aws-secret-key'
    })
    def test_credentials_loaded_from_environment(self):
        """Test that credentials are properly loaded from environment variables"""
        # Reload the module to pick up new environment variables
        import importlib
        importlib.reload(chukanchi_be)
        
        self.assertEqual(chukanchi_be.GOOGLE_OAUTH_CLIENT_ID, 'test-google-client-id')
        self.assertEqual(chukanchi_be.AWS_ACCESS_KEY_ID, 'test-aws-access-key')
        self.assertEqual(chukanchi_be.AWS_SECRET_ACCESS_KEY, 'test-aws-secret-key')

    @patch.dict(os.environ, {
        'GOOGLE_OAUTH_CLIENT_ID': 'test-google-client-id',
        'AWS_ACCESS_KEY_ID': 'test-aws-access-key',
        'AWS_SECRET_ACCESS_KEY': 'test-aws-secret-key'
    })
    def test_validate_credentials_success(self):
        """Test that validation passes when all credentials are set"""
        # Reload the module to pick up new environment variables
        import importlib
        importlib.reload(chukanchi_be)
        
        # Should not raise an exception
        self.assertTrue(chukanchi_be.validate_credentials())

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_credentials_missing_google_oauth(self):
        """Test that validation fails when Google OAuth client ID is missing"""
        # Reload the module to pick up cleared environment
        import importlib
        importlib.reload(chukanchi_be)
        
        with self.assertRaises(ValueError) as context:
            chukanchi_be.validate_credentials()
        self.assertIn('GOOGLE_OAUTH_CLIENT_ID', str(context.exception))

    @patch.dict(os.environ, {'GOOGLE_OAUTH_CLIENT_ID': 'test-id'}, clear=True)
    def test_validate_credentials_missing_aws_access_key(self):
        """Test that validation fails when AWS access key is missing"""
        # Reload the module to pick up new environment
        import importlib
        importlib.reload(chukanchi_be)
        
        with self.assertRaises(ValueError) as context:
            chukanchi_be.validate_credentials()
        self.assertIn('AWS_ACCESS_KEY_ID', str(context.exception))

    @patch.dict(os.environ, {
        'GOOGLE_OAUTH_CLIENT_ID': 'test-id',
        'AWS_ACCESS_KEY_ID': 'test-key'
    }, clear=True)
    def test_validate_credentials_missing_aws_secret_key(self):
        """Test that validation fails when AWS secret key is missing"""
        # Reload the module to pick up new environment
        import importlib
        importlib.reload(chukanchi_be)
        
        with self.assertRaises(ValueError) as context:
            chukanchi_be.validate_credentials()
        self.assertIn('AWS_SECRET_ACCESS_KEY', str(context.exception))


if __name__ == '__main__':
    unittest.main()
