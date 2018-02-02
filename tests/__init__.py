import os

# Need to use Env VAR to set cred file path
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = 'tests/aws_creds_file'

