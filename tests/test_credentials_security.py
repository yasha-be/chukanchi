import unittest
import os
import sys
sys.path.insert(0, '/workspace')

from chukanchi_be import CredentialsManager


class TestCredentialsSecurity(unittest.TestCase):
    """Test suite to verify that credentials are handled securely"""
    
    def setUp(self):
        """Set up test environment"""
        # Clear any existing environment variables
        for var in ['GOOGLE_OAUTH_KEY', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
            if var in os.environ:
                del os.environ[var]
    
    def tearDown(self):
        """Clean up test environment"""
        # Clear any test environment variables
        for var in ['GOOGLE_OAUTH_KEY', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
            if var in os.environ:
                del os.environ[var]
    
    def test_no_hardcoded_credentials_in_source(self):
        """Test that no hardcoded credentials exist in the source code"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check that no hardcoded AWS keys are present
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', content, 
                        "Hardcoded AWS Access Key ID found in source code")
        self.assertNotIn('o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', content,
                        "Hardcoded AWS Secret Access Key found in source code")
        
        # Check that no hardcoded Google OAuth keys are present
        self.assertNotIn('092625-01234567890123456789abcdefghijKL.apps.googleusercontent.com', content,
                        "Hardcoded Google OAuth key found in source code")
    
    def test_credentials_from_environment_variables(self):
        """Test that credentials are retrieved from environment variables"""
        # Set test environment variables
        os.environ['GOOGLE_OAUTH_KEY'] = 'test_google_key'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_aws_key_id'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_aws_secret'
        
        # Test that credentials are retrieved correctly
        self.assertEqual(CredentialsManager.get_google_oauth_key(), 'test_google_key')
        self.assertEqual(CredentialsManager.get_aws_access_key_id(), 'test_aws_key_id')
        self.assertEqual(CredentialsManager.get_aws_secret_access_key(), 'test_aws_secret')
    
    def test_empty_credentials_when_env_vars_not_set(self):
        """Test that empty strings are returned when environment variables are not set"""
        self.assertEqual(CredentialsManager.get_google_oauth_key(), '')
        self.assertEqual(CredentialsManager.get_aws_access_key_id(), '')
        self.assertEqual(CredentialsManager.get_aws_secret_access_key(), '')
    
    def test_validation_fails_with_missing_credentials(self):
        """Test that validation fails when required credentials are missing"""
        with self.assertRaises(ValueError) as context:
            CredentialsManager.validate_credentials()
        
        self.assertIn('Missing required environment variables', str(context.exception))
    
    def test_validation_passes_with_all_credentials(self):
        """Test that validation passes when all required credentials are present"""
        # Set all required environment variables
        os.environ['GOOGLE_OAUTH_KEY'] = 'test_google_key'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_aws_key_id'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_aws_secret'
        
        # Validation should pass
        self.assertTrue(CredentialsManager.validate_credentials())


if __name__ == '__main__':
    unittest.main()
