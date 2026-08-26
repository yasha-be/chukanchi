import unittest
import os
import sys
import tempfile
from unittest.mock import patch

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSecurityFix(unittest.TestCase):
    """Test that hardcoded credentials have been removed and proper configuration is used."""
    
    def test_no_hardcoded_credentials_in_file(self):
        """Test that the file doesn't contain any hardcoded credentials."""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check that no hardcoded AWS keys are present
        self.assertNotIn('AKIAIOSFODNN7EXAMPLE', content, 
                        "Hardcoded AWS Access Key ID found in file")
        self.assertNotIn('o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', content,
                        "Hardcoded AWS Secret Access Key found in file")
        
        # Check that no hardcoded Google OAuth keys are present
        self.assertNotIn('092625-01234567890123456789abcdefghijKL.apps.googleusercontent.com', content,
                        "Hardcoded Google OAuth key found in file")
        
        # Verify that environment variable usage is present
        self.assertIn('os.environ.get', content,
                     "Environment variable usage not found")
        self.assertIn('GOOGLE_OAUTH_CLIENT_ID', content,
                     "Google OAuth client ID environment variable not configured")
        self.assertIn('AWS_ACCESS_KEY_ID', content,
                     "AWS Access Key ID environment variable not configured")
        self.assertIn('AWS_SECRET_ACCESS_KEY', content,
                     "AWS Secret Access Key environment variable not configured")
    
    @patch.dict(os.environ, {
        'GOOGLE_OAUTH_CLIENT_ID': 'test_google_client_id',
        'AWS_ACCESS_KEY_ID': 'test_aws_key_id',
        'AWS_SECRET_ACCESS_KEY': 'test_aws_secret_key'
    })
    def test_module_loads_with_environment_variables(self):
        """Test that the module loads successfully when environment variables are set."""
        try:
            # Remove the module from cache if it exists
            if 'chukanchi_be' in sys.modules:
                del sys.modules['chukanchi_be']
            
            import chukanchi_be
            
            # Verify that the variables are set correctly
            self.assertEqual(chukanchi_be.GOOGLE_OAUTH_CLIENT_ID, 'test_google_client_id')
            self.assertEqual(chukanchi_be.AWS_ACCESS_KEY_ID, 'test_aws_key_id')
            self.assertEqual(chukanchi_be.AWS_SECRET_ACCESS_KEY, 'test_aws_secret_key')
            
        except Exception as e:
            self.fail(f"Module failed to load with environment variables: {e}")
    
    def test_module_raises_error_without_environment_variables(self):
        """Test that the module raises appropriate errors when environment variables are missing."""
        # Clear environment variables
        env_vars_to_clear = ['GOOGLE_OAUTH_CLIENT_ID', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
        
        with patch.dict(os.environ, {}, clear=True):
            # Remove the module from cache if it exists
            if 'chukanchi_be' in sys.modules:
                del sys.modules['chukanchi_be']
            
            with self.assertRaises(ValueError) as context:
                import chukanchi_be
            
            # Should raise an error about missing environment variables
            self.assertIn("environment variable is required", str(context.exception))


if __name__ == '__main__':
    unittest.main()
