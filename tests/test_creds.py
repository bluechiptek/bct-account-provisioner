import pytest

import provisioner.creds as creds

# Todo Paramterize fixture so that the saame test doesn't need to be duped
# https://docs.pytest.org/en/latest/parametrize.html
@pytest.fixture
def aws_creds_file_string():
    with open("tests/aws_creds_file") as credsfile:
        return credsfile.read()


@pytest.fixture
def aws_creds_file_obj():
    return open("tests/aws_creds_file")


def test_profiles_no_filters_obj(aws_creds_file_obj):
    credsfile = creds.AwsCredsFile(aws_creds_file_obj)
    profiles = credsfile.profiles
    expected_profiles = ['default',
                        'profile-include1',
                        'profile-include2',
                        'profile-exclude1',
                        'profile-exclude2']
    assert profiles == expected_profiles


def test_profiles_no_filters_string(aws_creds_file_string):
    credsfile = creds.AwsCredsFile(aws_creds_file_string)
    profiles = credsfile.profiles
    expected_profiles = ['default',
                        'profile-include1',
                        'profile-include2',
                        'profile-exclude1',
                        'profile-exclude2']
    assert profiles == expected_profiles

