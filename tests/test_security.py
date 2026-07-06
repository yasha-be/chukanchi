import unittest
import re
import os

class TestSecurity(unittest.TestCase):
    """Test suite to ensure no hardcoded credentials are present in the codebase."""
    
    def test_no_hardcoded_aws_keys(self):
        """Test that no hardcoded AWS access keys are present in the code."""
        # AWS Access Key patterns
        aws_access_key_pattern = r'AKIA[0-9A-Z]{16}'
        aws_secret_key_pattern = r'[A-Za-z0-9/+=]{40}'
        
        # Read the main application file
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for AWS access key patterns
        aws_keys_found = re.findall(aws_access_key_pattern, content)
        self.assertEqual(len(aws_keys_found), 0, 
                        f"Found hardcoded AWS access keys: {aws_keys_found}")
        
        # Check that we're using environment variables instead
        self.assertIn('os.getenv', content, 
                     "Code should use os.getenv() for accessing credentials")
        self.assertIn('AWS_ACCESS_KEY_ID', content,
                     "Code should reference AWS_ACCESS_KEY_ID environment variable")
        self.assertIn('AWS_SECRET_ACCESS_KEY', content,
                     "Code should reference AWS_SECRET_ACCESS_KEY environment variable")
    
    def test_no_hardcoded_google_oauth_keys(self):
        """Test that no hardcoded Google OAuth keys are present in the code."""
        # Google OAuth client ID pattern
        google_oauth_pattern = r'\d+-[a-zA-Z0-9]{32}\.apps\.googleusercontent\.com'
        
        # Read the main application file
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for Google OAuth patterns
        oauth_keys_found = re.findall(google_oauth_pattern, content)
        self.assertEqual(len(oauth_keys_found), 0,
                        f"Found hardcoded Google OAuth keys: {oauth_keys_found}")
        
        # Check that we're using environment variables instead
        self.assertIn('GOOGLE_OAUTH_CLIENT_ID', content,
                     "Code should reference GOOGLE_OAUTH_CLIENT_ID environment variable")
    
    def test_no_example_credentials(self):
        """Test that no example credentials from AWS documentation are present."""
        example_credentials = [
            'AKIAIOSFODNN7EXAMPLE',
            'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            'AKIADEEPFENCEEXAMPLE'
        ]
        
        # Read the main application file
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        for credential in example_credentials:
            self.assertNotIn(credential, content,
                           f"Found example credential '{credential}' in code")
    
    def test_environment_variable_usage(self):
        """Test that the code properly uses environment variables for configuration."""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Ensure we import os module
        self.assertIn('import os', content, "Code should import os module")
        
        # Ensure we use os.getenv with appropriate fallbacks
        self.assertIn("os.getenv('GOOGLE_OAUTH_CLIENT_ID'", content)
        self.assertIn("os.getenv('AWS_ACCESS_KEY_ID'", content)
        self.assertIn("os.getenv('AWS_SECRET_ACCESS_KEY'", content)

if __name__ == '__main__':
    unittest.main()
