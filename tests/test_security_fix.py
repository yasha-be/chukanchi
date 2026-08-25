import unittest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import chukanchi_be


class TestSecurityFix(unittest.TestCase):
    """Test that hardcoded credentials have been removed and proper configuration is used."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear any existing environment variables
        for key in ['GOOGLE_OAUTH_CLIENT_ID', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
            if key in os.environ:
                del os.environ[key]
    
    def test_no_hardcoded_credentials_in_source(self):
        """Test that no hardcoded credentials exist in the source code."""
        with open('chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check that no hardcoded AWS keys are present
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', content, 
                        "Hardcoded AWS Access Key ID found in source code")
        self.assertNotIn('o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', content,
                        "Hardcoded AWS Secret Access Key found in source code")
        
        # Check that no hardcoded Google OAuth keys are present
        self.assertNotIn('092625-01234567890123456789abcdefghijKL.apps.googleusercontent.com', content,
                        "Hardcoded Google OAuth Client ID found in source code")
    
    def test_google_oauth_config_requires_env_var(self):
        """Test that Google OAuth configuration requires environment variable."""
        with self.assertRaises(ValueError) as context:
            chukanchi_be.get_google_oauth_config()
        
        self.assertIn("GOOGLE_OAUTH_CLIENT_ID environment variable is required", 
                     str(context.exception))
    
    def test_aws_credentials_require_env_vars(self):
        """Test that AWS credentials require environment variables."""
        with self.assertRaises(ValueError) as context:
            chukanchi_be.get_aws_credentials()
        
        self.assertIn("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required",
                     str(context.exception))
    
    def test_google_oauth_config_with_env_var(self):
        """Test that Google OAuth configuration works with environment variable."""
        test_client_id = "test-client-id.apps.googleusercontent.com"
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = test_client_id
        
        result = chukanchi_be.get_google_oauth_config()
        self.assertEqual(result, test_client_id)
    
    def test_aws_credentials_with_env_vars(self):
        """Test that AWS credentials work with environment variables."""
        test_access_key = "AKIATEST123456789"
        test_secret_key = "test-secret-key-123"
        
        os.environ['AWS_ACCESS_KEY_ID'] = test_access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = test_secret_key
        
        result = chukanchi_be.get_aws_credentials()
        expected = {
            'access_key_id': test_access_key,
            'secret_access_key': test_secret_key
        }
        self.assertEqual(result, expected)
    
    def test_partial_aws_credentials_fail(self):
        """Test that partial AWS credentials fail appropriately."""
        # Test with only access key
        os.environ['AWS_ACCESS_KEY_ID'] = "AKIATEST123456789"
        
        with self.assertRaises(ValueError):
            chukanchi_be.get_aws_credentials()
        
        # Clear and test with only secret key
        del os.environ['AWS_ACCESS_KEY_ID']
        os.environ['AWS_SECRET_ACCESS_KEY'] = "test-secret-key"
        
        with self.assertRaises(ValueError):
            chukanchi_be.get_aws_credentials()


if __name__ == '__main__':
    unittest.main()
