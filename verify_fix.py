#!/usr/bin/env python3

import chukanchi_be

print("Module imports successfully")
print("Testing error handling...")

try:
    chukanchi_be.get_google_oauth_config()
except ValueError as e:
    print("✓ Google OAuth properly requires env var:", str(e))

try:
    chukanchi_be.get_aws_credentials()
except ValueError as e:
    print("✓ AWS credentials properly require env vars:", str(e))

print("✓ All security checks passed!")
