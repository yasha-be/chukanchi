import unittest
import os
import sys
import re

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSecurityFix(unittest.TestCase):
    
    def test_no_hardcoded_credentials(self):
        """Test that no hardcoded credentials are present in the chukanchi_be.py file"""
        
        # Read the file content
        with open('chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Patterns for common credential formats
        credential_patterns = [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID pattern
            r'[0-9]+-[a-zA-Z0-9]{32}\.apps\.googleusercontent\.com',  # Google OAuth Client ID pattern
            r'[A-Za-z0-9/+=]{40}',  # AWS Secret Access Key pattern (40 chars base64)
        ]
        
        # Check that no hardcoded credentials are found
        for pattern in credential_patterns:
            matches = re.findall(pattern, content)
            # Filter out the example comments
            actual_matches = [match for match in matches if not any(
                comment_word in content[max(0, content.find(match) - 100):content.find(match) + 100].lower()
                for comment_word in ['#', 'example', 'your-', 'export']
            )]
            self.assertEqual(len(actual_matches), 0, 
                           f"Found hardcoded credential pattern: {pattern} - matches: {actual_matches}")
    
    def test_environment_variables_used(self):
        """Test that environment variables are properly used for credentials"""
        
        # Clean up any existing environment variables first
        env_vars = ['GOOGLE_OAUTH_CLIENT_ID', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
        original_values = {}
        for var in env_vars:
            if var in os.environ:
                original_values[var] = os.environ[var]
                del os.environ[var]
        
        # Reload the module to pick up clean environment
        if 'chukanchi_be' in sys.modules:
            del sys.modules['chukanchi_be']
        
        import chukanchi_be
        
        # Test that the variables exist and use os.getenv
        self.assertTrue(hasattr(chukanchi_be, 'GOOGLE_OAUTH_CLIENT_ID'))
        self.assertTrue(hasattr(chukanchi_be, 'AWS_ACCESS_KEY_ID'))
        self.assertTrue(hasattr(chukanchi_be, 'AWS_SECRET_ACCESS_KEY'))
        
        # Test default values when environment variables are not set
        self.assertEqual(chukanchi_be.GOOGLE_OAUTH_CLIENT_ID, '')
        self.assertEqual(chukanchi_be.AWS_ACCESS_KEY_ID, '')
        self.assertEqual(chukanchi_be.AWS_SECRET_ACCESS_KEY, '')
        
        # Restore original environment variables
        for var, value in original_values.items():
            os.environ[var] = value
    
    def test_environment_variables_override(self):
        """Test that environment variables properly override default values"""
        
        # Set test environment variables
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = 'test-client-id'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-access-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret-key'
        
        # Reload the module to pick up new environment variables
        if 'chukanchi_be' in sys.modules:
            del sys.modules['chukanchi_be']
        
        import chukanchi_be
        
        # Test that environment variables are used
        self.assertEqual(chukanchi_be.GOOGLE_OAUTH_CLIENT_ID, 'test-client-id')
        self.assertEqual(chukanchi_be.AWS_ACCESS_KEY_ID, 'test-access-key')
        self.assertEqual(chukanchi_be.AWS_SECRET_ACCESS_KEY, 'test-secret-key')
        
        # Clean up environment variables
        del os.environ['GOOGLE_OAUTH_CLIENT_ID']
        del os.environ['AWS_ACCESS_KEY_ID']
        del os.environ['AWS_SECRET_ACCESS_KEY']

if __name__ == '__main__':
    unittest.main()
