import botocore
import moto
import pytest

import provisioner.accounts as accounts


@pytest.fixture
def aws_creds_file_string():
    with open("provisioner/tests/aws_creds_file") as credsfile:
        return credsfile.read()


@pytest.fixture
def aws_creds_file_obj():
    return open("provisioner/tests/aws_creds_file")


# Run test using both accounts file as string or as object
@pytest.mark.parametrize('aws_creds_file',
                         [aws_creds_file_string(), aws_creds_file_obj()])
def test_profiles_no_filters(aws_creds_file):
    credsfile = accounts.AwsCredsFile(aws_creds_file)
    profiles = credsfile.profiles
    expected_profiles = ['default',
                         'profile-include1',
                         'profile-include2',
                         'profile-exclude1',
                         'profile-exclude2']
    assert profiles == expected_profiles


def test_profiles_include_list(aws_creds_file_string):
    credsfile = accounts.AwsCredsFile(aws_creds_file_string,
                                      include=['profile-include1',
                                               'profile-include2'])
    profiles = credsfile.profiles
    expected_profiles = ['profile-include1',
                         'profile-include2']
    assert profiles == expected_profiles


def test_profiles_include_regex(aws_creds_file_string):
    credsfile = accounts.AwsCredsFile(aws_creds_file_string,
                                      include='.*include*')
    profiles = credsfile.profiles
    expected_profiles = ['profile-include1',
                         'profile-include2']
    assert profiles == expected_profiles


def test_profiles_exclude_list(aws_creds_file_string):
    credsfile = accounts.AwsCredsFile(aws_creds_file_string,
                                      exclude=['profile-exclude1',
                                               'profile-exclude2'])
    profiles = credsfile.profiles
    expected_profiles = ['default',
                         'profile-include1',
                         'profile-include2']
    assert profiles == expected_profiles


def test_profiles_exclude_regex(aws_creds_file_string):
    credsfile = accounts.AwsCredsFile(aws_creds_file_string,
                                      exclude='.*exclude*')
    profiles = credsfile.profiles
    expected_profiles = ['default',
                         'profile-include1',
                         'profile-include2']
    assert profiles == expected_profiles


def test_profiles_include_exclude(aws_creds_file_string):
    credsfile = accounts.AwsCredsFile(aws_creds_file_string,
                                      include='.*profile*',
                                      exclude='.*exclude*')
    profiles = credsfile.profiles
    expected_profiles = ['profile-include1',
                         'profile-include2']
    assert profiles == expected_profiles


@moto.mock_sts
def test_account_object():
    default_account = accounts.AwsAccount('default')
    assert default_account.id == '123456789012'


def test_account_object_invalid_profile():
    with pytest.raises(botocore.exceptions.ProfileNotFound):
        accounts.AwsAccount('invalid')
