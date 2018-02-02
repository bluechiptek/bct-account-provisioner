import _io
import configparser
import logging
import re

import boto3

logger = logging.getLogger(__name__)


class AwsAccount:
    """Contains metadata and connection info for each account

    Args:
        profile_name: Name of the profile used to build the AwsAccount object.

    """

    def __init__(self, profile_name):
        self._profile_name = profile_name
        self._session = boto3.session.Session(profile_name=profile_name)
        self._id = self._session.client('sts').get_caller_identity()['Account']

    @property
    def id(self):
        return self._id

    @property
    def profile_name(self):
        return self._profile_name

    @property
    def session(self):
        return self._session


class AwsAccounts:
    """Provides a list of target AwsAccount objects that will be provisioned.

    credentials files defaults to ~/.aws/credentials or needs to be overrided
    via the AWS_SHARED_CREDENTIALS_FILE env var

    Args:
        include:    A list or regex of profile names that should be
                    provisioned.
        exclude:    A list or regex of profiles names that should not be
                    provisioned. Exclude is processed before includes.
    """

    def __init__(self, include=None, exclude=None):
        self._include = include
        self._exclude = exclude

    @property
    def target_accounts(self):
        """Returns a list of profile names to be provisioned."""
        profiles = boto3.Session().available_profiles
        target_accounts = []
        for profile in profiles:
            if self._exclude and self._match(profile, self._exclude):
                logger.info("Excluding profile {}".format(profile))
                continue
            elif self._include:
                if self._match(profile, self._include):
                    logger.info("Including profile {}".format(profile))
                    account = AwsAccount(profile)
                    target_accounts.append(account)
            else:
                logger.info("Including profile {}".format(profile))
                account = AwsAccount(profile)
                target_accounts.append(account)
        return target_accounts

    @staticmethod
    def _match(item, criteria):
        """Determines if an item matches a criteria.

        Criteria is either a list or a regex. Returns True or False.
        """
        if type(criteria) is list:
            return item in criteria
        else:
            # If not list, assume regex
            return re.match(criteria, item)

