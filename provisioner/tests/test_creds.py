import pytest

import provisioner.creds as creds


@pytest.fixture
def aws_creds_file_string():
    with open("provisioner/tests/aws_creds_file") as credsfile:
        return credsfile.read()


@pytest.fixture
def aws_creds_file_obj():
    return open("provisioner/tests/aws_creds_file")


# Run test using both creds file as string or as object
@pytest.mark.parametrize('aws_creds_file',
                         [aws_creds_file_string(), aws_creds_file_obj()])
def test_profiles_no_filters(aws_creds_file):
    credsfile = creds.AwsCredsFile(aws_creds_file)
    profiles = credsfile.profiles
    expected_profiles = ['default',
                        'profile-include1',
                        'profile-include2',
                        'profile-exclude1',
                        'profile-exclude2']
    assert profiles == expected_profiles

