#!/usr/bin/env python3
"""
Security test to ensure no hardcoded credentials are present in the codebase.
"""
import re
import os

def test_no_hardcoded_credentials():
    """Test that no hardcoded credentials are present in chukanchi_be.py"""
    
    # Read the file content
    with open('/workspace/chukanchi_be.py', 'r') as f:
        content = f.read()
    
    # Patterns for sensitive data that should not be hardcoded
    sensitive_patterns = [
        r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID pattern
        r'[0-9]+-[a-zA-Z0-9]{32}\.apps\.googleusercontent\.com',  # Google OAuth Client ID pattern
        r'[A-Za-z0-9/+=]{40}',  # AWS Secret Access Key pattern (40 chars base64-like)
    ]
    
    # Check that no sensitive patterns are found as hardcoded values
    for pattern in sensitive_patterns:
        matches = re.findall(pattern, content)
        # Filter out placeholder/example values
        real_matches = [match for match in matches if not any(placeholder in match.lower() 
                       for placeholder in ['example', 'your-', 'placeholder', 'xxx'])]
        
        assert len(real_matches) == 0, f"Found potential hardcoded credential: {real_matches}"
    
    # Verify that environment variable usage is present
    assert 'os.environ.get' in content, "Environment variable usage not found"
    assert 'GOOGLE_OAUTH_CLIENT_ID' in content, "Google OAuth configuration not found"
    assert 'AWS_ACCESS_KEY_ID' in content, "AWS Access Key configuration not found"
    assert 'AWS_SECRET_ACCESS_KEY' in content, "AWS Secret Access Key configuration not found"
    
    print("✅ Security test passed: No hardcoded credentials found")
    print("✅ Environment variable configuration properly implemented")

def test_file_structure():
    """Test that the file has proper Python structure"""
    with open('/workspace/chukanchi_be.py', 'r') as f:
        content = f.read()
    
    # Should start with import statement
    assert content.startswith('import os'), "File should start with proper imports"
    
    # Should contain proper variable assignments
    assert 'GOOGLE_OAUTH_CLIENT_ID =' in content, "Google OAuth client ID variable not defined"
    assert 'AWS_ACCESS_KEY_ID =' in content, "AWS Access Key ID variable not defined"
    assert 'AWS_SECRET_ACCESS_KEY =' in content, "AWS Secret Access Key variable not defined"
    
    print("✅ File structure test passed")

if __name__ == '__main__':
    test_no_hardcoded_credentials()
    test_file_structure()
    print("🎉 All security tests passed!")
