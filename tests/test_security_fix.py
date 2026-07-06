import unittest
import os
import sys
import tempfile

sys.path.insert(0, '/workspace')

from chukanchi_be import SecurityConfig, validate_credentials


class TestSecurityFix(unittest.TestCase):
    """
    Test suite to verify that the security vulnerability has been fixed.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.original_env = os.environ.copy()
    
    def tearDown(self):
        """Clean up test environment."""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_no_hardcoded_credentials_in_file(self):
        """Test that no hardcoded credentials exist in the source file."""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check that no hardcoded Google OAuth client IDs are present
        self.assertNotIn('092625-01234567890123456789abcdefghijKL.apps.googleusercontent.com', content)
        
        # Check that no hardcoded AWS access keys are present
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', content)
        self.assertNotIn('o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', content)
        self.assertNotIn('AKIADEEPFENCEEXAMPLE', content)
    
    def test_security_config_uses_environment_variables(self):
        """Test that SecurityConfig properly uses environment variables."""
        # Clear environment variables
        for key in ['GOOGLE_OAUTH_CLIENT_ID', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
            if key in os.environ:
                del os.environ[key]
        
        config = SecurityConfig()
        
        # Test that methods return empty strings when env vars are not set
        self.assertEqual(config.get_google_oauth_client_id(), '')
        self.assertEqual(config.get_aws_access_key_id(), '')
        self.assertEqual(config.get_aws_secret_access_key(), '')
        
        # Set environment variables and test that they are returned
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = 'test_google_client_id'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_aws_access_key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_aws_secret_key'
        
        self.assertEqual(config.get_google_oauth_client_id(), 'test_google_client_id')
        self.assertEqual(config.get_aws_access_key_id(), 'test_aws_access_key')
        self.assertEqual(config.get_aws_secret_access_key(), 'test_aws_secret_key')
    
    def test_validate_credentials_with_missing_env_vars(self):
        """Test that validate_credentials returns False when env vars are missing."""
        # Clear environment variables
        for key in ['GOOGLE_OAUTH_CLIENT_ID', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
            if key in os.environ:
                del os.environ[key]
        
        self.assertFalse(validate_credentials())
    
    def test_validate_credentials_with_all_env_vars_set(self):
        """Test that validate_credentials returns True when all env vars are set."""
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = 'test_google_client_id'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_aws_access_key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_aws_secret_key'
        
        self.assertTrue(validate_credentials())
    
    def test_validate_credentials_with_partial_env_vars(self):
        """Test that validate_credentials returns False when only some env vars are set."""
        # Clear all environment variables first
        for key in ['GOOGLE_OAUTH_CLIENT_ID', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
            if key in os.environ:
                del os.environ[key]
        
        # Test with only Google OAuth client ID set
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = 'test_google_client_id'
        self.assertFalse(validate_credentials())
        
        # Test with only AWS access key set
        del os.environ['GOOGLE_OAUTH_CLIENT_ID']
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_aws_access_key'
        self.assertFalse(validate_credentials())
        
        # Test with only AWS secret key set
        del os.environ['AWS_ACCESS_KEY_ID']
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_aws_secret_key'
        self.assertFalse(validate_credentials())


if __name__ == '__main__':
    unittest.main()
