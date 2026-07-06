# chukanchi

## Security Configuration

This application requires the following environment variables to be set:

- `GOOGLE_OAUTH_CLIENT_ID`: Your Google OAuth client ID
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID  
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key

### Setup

1. Copy `.env.example` to `.env`
2. Fill in your actual credentials in the `.env` file
3. Source the environment variables before running the application

```bash
cp .env.example .env
# Edit .env with your credentials
source .env
python chukanchi_be.py
```

**Important**: Never commit actual credentials to version control. The `.env` file should be added to `.gitignore`.
