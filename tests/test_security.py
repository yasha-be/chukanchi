import unittest
import os
import re
import sys

class TestSecurityCompliance(unittest.TestCase):
    
    def setUp(self):
        self.chukanchi_be_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chukanchi_be.py')
    
    def test_no_hardcoded_secrets(self):
        """Test that no hardcoded API keys or secrets are present in the code"""
        with open(self.chukanchi_be_path, 'r') as f:
            content = f.read()
        
        # Patterns for common API keys and secrets
        secret_patterns = [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID
            r'sk_[a-zA-Z0-9]{24,}',  # Stripe Secret Key
            r'pk_[a-zA-Z0-9]{24,}',  # Stripe Publishable Key
            r'[0-9]+-[a-zA-Z0-9]{32}\.apps\.googleusercontent\.com',  # Google OAuth Client ID
            r'[a-zA-Z0-9/+=]{40,}',  # Generic base64 encoded secrets (AWS Secret Access Key pattern)
        ]
        
        for pattern in secret_patterns:
            matches = re.findall(pattern, content)
            self.assertEqual(len(matches), 0, 
                           f"Found potential hardcoded secret matching pattern {pattern}: {matches}")
    
    def test_environment_variables_used(self):
        """Test that environment variables are properly used for configuration"""
        with open(self.chukanchi_be_path, 'r') as f:
            content = f.read()
        
        # Check that os.getenv is used for sensitive configuration
        self.assertIn('os.getenv', content, "Environment variables should be used for configuration")
        self.assertIn('GOOGLE_OAUTH_CLIENT_ID', content, "Google OAuth Client ID should be configurable")
        self.assertIn('AWS_ACCESS_KEY_ID', content, "AWS Access Key ID should be configurable")
        self.assertIn('AWS_SECRET_ACCESS_KEY', content, "AWS Secret Access Key should be configurable")
    
    def test_no_example_keys_in_code(self):
        """Test that no example/dummy keys are hardcoded in the actual code"""
        with open(self.chukanchi_be_path, 'r') as f:
            content = f.read()
        
        # Remove comments from content for this test
        lines = content.split('\n')
        code_lines = [line for line in lines if not line.strip().startswith('#')]
        code_content = '\n'.join(code_lines)
        
        example_patterns = [
            'AKIAIOSFODNN7EXAMPLE',
            'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            '092625-01234567890123456789abcdefghijKL',
        ]
        
        for pattern in example_patterns:
            self.assertNotIn(pattern, code_content, 
                           f"Example/dummy key should not be present in code: {pattern}")

if __name__ == '__main__':
    unittest.main()
