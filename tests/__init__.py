import os
import pathlib

# Need to use Env VAR to set cred file path
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = 'tests/aws_creds_file'

VALID_TEMPLATE1_URL = 'file://tests/cfn_valid_template1.yaml'
VALID_TEMPLATE2_URL = 'file://tests/cfn_valid_template2.yaml'
