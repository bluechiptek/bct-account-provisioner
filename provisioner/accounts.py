import _io
import configparser
import re


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
                continue
            elif self._include:
                if self._match(profile, self._include):
                    target_profiles.append(profile)
            else:
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
