import unittest
import re
import os


class TestSecurity(unittest.TestCase):
    """Test suite to ensure no hardcoded credentials are present in the codebase."""
    
    def test_no_hardcoded_credentials(self):
        """Test that no hardcoded credentials are present in chukanchi_be.py"""
        
        # Patterns to detect common credential formats
        credential_patterns = [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID pattern
            r'[0-9]{6,12}-[a-zA-Z0-9]{32}\.apps\.googleusercontent\.com',  # Google OAuth client ID
            r'[A-Za-z0-9/+=]{40}',  # AWS Secret Access Key pattern (base64-like)
        ]
        
        # Read the main application file
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for hardcoded credential patterns
        for pattern in credential_patterns:
            matches = re.findall(pattern, content)
            # Filter out environment variable references and comments
            actual_credentials = []
            for match in matches:
                # Skip if it's part of an environment variable call or comment
                if f"os.getenv('{match}'" not in content and \
                   f'export {match}' not in content and \
                   not any(line.strip().startswith('#') and match in line 
                          for line in content.split('\n')):
                    actual_credentials.append(match)
            
            self.assertEqual(len(actual_credentials), 0, 
                           f"Found hardcoded credentials matching pattern {pattern}: {actual_credentials}")
    
    def test_uses_environment_variables(self):
        """Test that the application properly uses environment variables for credentials."""
        
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check that environment variables are used for sensitive data
        self.assertIn('os.getenv(', content, 
                     "Application should use os.getenv() for configuration")
        self.assertIn('GOOGLE_OAUTH_CLIENT_ID', content,
                     "Should reference GOOGLE_OAUTH_CLIENT_ID environment variable")
        self.assertIn('AWS_ACCESS_KEY_ID', content,
                     "Should reference AWS_ACCESS_KEY_ID environment variable")
        self.assertIn('AWS_SECRET_ACCESS_KEY', content,
                     "Should reference AWS_SECRET_ACCESS_KEY environment variable")
    
    def test_no_example_credentials_in_code(self):
        """Test that no example/dummy credentials are hardcoded in the actual code."""
        
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Common example/dummy credential values that should not be in code
        forbidden_values = [
            'AKIAIOSFODNN7EXAMPLE',
            'o2/+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            '092625-01234567890123456789abcdefghijKL.apps.googleusercontent.com',
            'AKIADEEPFENCEEXAMPLE'
        ]
        
        for forbidden_value in forbidden_values:
            # Only fail if the value appears outside of comments
            lines_with_value = [line for line in content.split('\n') 
                              if forbidden_value in line and not line.strip().startswith('#')]
            self.assertEqual(len(lines_with_value), 0,
                           f"Found forbidden example credential value: {forbidden_value}")


if __name__ == '__main__':
    unittest.main()
