import unittest
import os
import sys
import re

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chukanchi_be import Config


class TestSecurityFix(unittest.TestCase):
    """Test cases to verify that hardcoded credentials have been removed"""
    
    def test_no_hardcoded_aws_keys(self):
        """Test that no hardcoded AWS access keys exist in the file"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for AWS access key patterns
        aws_key_patterns = [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID pattern
            r'AKIADEEPFENCEEXAMPLE',  # Specific key from the SAST finding
            r'AKIAIOSFODNN7EXAMPLE',  # Example keys that were in the file
        ]
        
        for pattern in aws_key_patterns:
            matches = re.findall(pattern, content)
            self.assertEqual(len(matches), 0, 
                           f"Found hardcoded AWS key pattern: {pattern}")
    
    def test_no_hardcoded_google_oauth_keys(self):
        """Test that no hardcoded Google OAuth keys exist in the file"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for Google OAuth client ID patterns
        google_patterns = [
            r'\d+-[a-zA-Z0-9]{32}\.apps\.googleusercontent\.com',
            r'092625-01234567890123456789abcdefghijKL\.apps\.googleusercontent\.com'
        ]
        
        for pattern in google_patterns:
            matches = re.findall(pattern, content)
            self.assertEqual(len(matches), 0, 
                           f"Found hardcoded Google OAuth key pattern: {pattern}")
    
    def test_no_hardcoded_secret_keys(self):
        """Test that no hardcoded secret access keys exist in the file"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # Check for AWS secret key patterns
        secret_patterns = [
            r'o2/\+wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            r'[A-Za-z0-9/+=]{40}',  # General AWS secret key pattern
        ]
        
        for pattern in secret_patterns:
            matches = re.findall(pattern, content)
            # Filter out legitimate code patterns
            legitimate_matches = [m for m in matches if 'AWS_SECRET_ACCESS_KEY' not in m and 'environ.get' not in content[content.find(m)-50:content.find(m)+50]]
            self.assertEqual(len(legitimate_matches), 0, 
                           f"Found hardcoded secret key pattern: {pattern}")
    
    def test_config_class_exists(self):
        """Test that the Config class exists and has the required methods"""
        self.assertTrue(hasattr(Config, 'get_google_oauth_key'))
        self.assertTrue(hasattr(Config, 'get_aws_access_key_id'))
        self.assertTrue(hasattr(Config, 'get_aws_secret_access_key'))
    
    def test_config_methods_use_environment_variables(self):
        """Test that Config methods use environment variables"""
        # Test with no environment variables set
        self.assertEqual(Config.get_google_oauth_key(), '')
        self.assertEqual(Config.get_aws_access_key_id(), '')
        self.assertEqual(Config.get_aws_secret_access_key(), '')
        
        # Test with environment variables set
        os.environ['GOOGLE_OAUTH_CLIENT_ID'] = 'test_google_key'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_aws_key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_secret_key'
        
        self.assertEqual(Config.get_google_oauth_key(), 'test_google_key')
        self.assertEqual(Config.get_aws_access_key_id(), 'test_aws_key')
        self.assertEqual(Config.get_aws_secret_access_key(), 'test_secret_key')
        
        # Clean up environment variables
        del os.environ['GOOGLE_OAUTH_CLIENT_ID']
        del os.environ['AWS_ACCESS_KEY_ID']
        del os.environ['AWS_SECRET_ACCESS_KEY']
    
    def test_sast_finding_pattern_removed(self):
        """Test that the specific SAST finding pattern is removed"""
        with open('/workspace/chukanchi_be.py', 'r') as f:
            content = f.read()
        
        # The specific pattern from the SAST finding
        sast_pattern = r'\\=>\\AKIADEEPFENCEEXAMPLE'
        matches = re.findall(sast_pattern, content)
        self.assertEqual(len(matches), 0, 
                       "SAST finding pattern still exists in the file")


if __name__ == '__main__':
    unittest.main()
