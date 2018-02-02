import botocore
import moto
import pytest

from lib.accounts import AwsAccounts, AwsAccount


@moto.mock_sts
def test_profiles_no_filters():
    accounts = AwsAccounts().target_accounts
    profiles = [account.profile_name for account in accounts]
    expected_profiles = ['default',
                         'profile-include1',
                         'profile-include2',
                         'profile-exclude1',
                         'profile-exclude2']
    assert profiles.sort() == expected_profiles.sort()


@moto.mock_sts
def test_profiles_include_list():
    accounts = AwsAccounts(
                            include=['profile-include1',
                                     'profile-include2']
                           ).target_accounts
    profiles = [account.profile_name for account in accounts]
    expected_profiles = ['profile-include1',
                         'profile-include2']
    assert profiles.sort() == expected_profiles.sort()


@moto.mock_sts
def test_profiles_include_regex():
    accounts = AwsAccounts(
                            include='.*include*'
                           ).target_accounts
    profiles = [account.profile_name for account in accounts]
    expected_profiles = ['profile-include1',
                         'profile-include2']
    assert profiles.sort() == expected_profiles.sort()


@moto.mock_sts
def test_profiles_exclude_list():
    accounts = AwsAccounts(
                            exclude=['profile-exclude1',
                                     'profile-exclude2']
                           ).target_accounts
    profiles = [account.profile_name for account in accounts]
    expected_profiles = ['default',
                         'profile-include1',
                         'profile-include2']
    assert profiles.sort() == expected_profiles.sort()


@moto.mock_sts
def test_profiles_exclude_regex():
    accounts = AwsAccounts(
                            exclude='.*exclude*'
                           ).target_accounts
    profiles = [account.profile_name for account in accounts]
    expected_profiles = ['default',
                         'profile-include1',
                         'profile-include2']
    assert profiles.sort() == expected_profiles.sort()


@moto.mock_sts
def test_profiles_include_exclude():
    accounts = AwsAccounts(
                            include='.*profile*',
                            exclude='.*exclude*'
                           ).target_accounts
    profiles = [account.profile_name for account in accounts]
    expected_profiles = ['profile-include1',
                         'profile-include2']
    assert profiles.sort() == expected_profiles.sort()


@moto.mock_sts
def test_account_object():
    default_account = AwsAccount('default')
    assert default_account.id == '123456789012'


def test_account_object_invalid_profile():
    with pytest.raises(botocore.exceptions.ProfileNotFound):
        AwsAccount('invalid')
