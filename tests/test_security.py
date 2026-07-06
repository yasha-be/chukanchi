import unittest
import re
import os
import sys

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chukanchi_be


class TestSecurityVulnerabilities(unittest.TestCase):
    """Test suite to ensure no hardcoded credentials are present in the codebase."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = chukanchi_be.Config()
        
    def test_no_hardcoded_aws_keys(self):
        """Test that no hardcoded AWS access keys are present in the source code."""
        # Read the source file
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Patterns for AWS access keys (should not be found)
        aws_key_patterns = [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID pattern
            r'AKIADEEPFENCEEXAMPLE',  # Specific vulnerable key mentioned in the issue
            r'AKIAIOSFODNN7EXAMPLE',  # Example keys that were hardcoded
        ]
        
        for pattern in aws_key_patterns:
            matches = re.findall(pattern, content)
            self.assertEqual(len(matches), 0, 
                           f"Found hardcoded AWS key pattern '{pattern}' in source code: {matches}")
    
    def test_no_hardcoded_google_oauth_keys(self):
        """Test that no hardcoded Google OAuth keys are present in the source code."""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Pattern for Google OAuth client IDs (should not be found)
        google_oauth_pattern = r'\d+-[a-zA-Z0-9]{32}\.apps\.googleusercontent\.com'
        matches = re.findall(google_oauth_pattern, content)
        self.assertEqual(len(matches), 0, 
                        f"Found hardcoded Google OAuth client ID in source code: {matches}")
    
    def test_no_hardcoded_secret_keys(self):
        """Test that no hardcoded secret access keys are present in the source code."""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Pattern for AWS secret access keys (should not be found)
        secret_key_pattern = r'[A-Za-z0-9/+=]{40}'
        # Look for the specific vulnerable secret key
        vulnerable_secret = 'o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        
        self.assertNotIn(vulnerable_secret, content, 
                        "Found hardcoded AWS secret access key in source code")
    
    def test_config_uses_environment_variables(self):
        """Test that the Config class properly uses environment variables."""
        # Test with default values (when env vars are not set)
        config = chukanchi_be.Config()
        
        # Should return default placeholder values, not actual credentials
        google_client_id = config.get_google_oauth_client_id()
        aws_creds = config.get_aws_credentials()
        
        # Ensure these are placeholder values, not real credentials
        self.assertEqual(google_client_id, 'your-google-oauth-client-id')
        self.assertEqual(aws_creds['access_key_id'], 'your-aws-access-key-id')
        self.assertEqual(aws_creds['secret_access_key'], 'your-aws-secret-access-key')
    
    def test_config_respects_environment_variables(self):
        """Test that the Config class respects environment variables when set."""
        # Set test environment variables
        test_google_id = 'test-google-oauth-client-id'
        test_aws_key = 'test-aws-access-key'
        test_aws_secret = 'test-aws-secret-key'
        
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = test_google_id
        os.environ['AWS_ACCESS_KEY_ID'] = test_aws_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = test_aws_secret
        
        try:
            # Reload the module to pick up new environment variables
            import importlib
            importlib.reload(chukanchi_be)
            
            config = chukanchi_be.Config()
            
            self.assertEqual(config.get_google_oauth_client_id(), test_google_id)
            aws_creds = config.get_aws_credentials()
            self.assertEqual(aws_creds['access_key_id'], test_aws_key)
            self.assertEqual(aws_creds['secret_access_key'], test_aws_secret)
            
        finally:
            # Clean up environment variables
            del os.environ['GOOGLE_OAUTH_CLIENT_ID']
            del os.environ['AWS_ACCESS_KEY_ID']
            del os.environ['AWS_SECRET_ACCESS_KEY']
            # Reload module again to restore original state
            importlib.reload(chukanchi_be)


if __name__ == '__main__':
    unittest.main()
