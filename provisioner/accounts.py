import _io
import configparser
import logging
import re

import boto3


class AwsCredsFile:
    """Parses and provides information on an AWS credentials file.

    Args:
        credsfile:  A string object with the contents of an AWS credentials
                    file. If a file object (_io.TextIOWrapper) is passed then
                    the contents of the file will be read.
        include:    A list or regex of profile names that should be
                    provisioned.
        exclude:    A list or regex of profiles names that should not be
                    provisioned. Exclude is processed before includes.
    """

    def __init__(self, credsfile, include=None, exclude=None):
        if type(credsfile) == _io.TextIOWrapper:
            self._credsfile = credsfile.read()
        elif type(credsfile) == str:
            self._credsfile = credsfile
        else:
            raise TypeError(
                "credsfile is {} and should be string or file object.".format(
                    type(credsfile)
                )
            )
        self._include = include
        self._exclude = exclude

    @property
    def profiles(self):
        """Returns a list of profile names to be provisioned."""
        config = configparser.ConfigParser()
        config.read_string(self._credsfile)
        target_profiles = []
        for profile in config.sections():
            if self._exclude and self._match(profile, self._exclude):
                logging.info("Excluding profile {}".format(profile))
                continue
            elif self._include:
                if self._match(profile, self._include):
                    logging.info("Including profile {}".format(profile))
                    target_profiles.append(profile)
            else:
                logging.info("Including profile {}".format(profile))
                target_profiles.append(profile)
        return target_profiles

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

