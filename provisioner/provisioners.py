import sys

from provisioner.accounts import AwsCredsFile
from provisioner.stacks import Stack, Template


class AwsProvisioner():

    def __init__(self,
                 creds_file_path,
                 cfn_template_path,
                 include_profiles=None,
                 exclude_profiles=None):
        with open(creds_file_path) as creds_file:
            self._creds = AwsCredsFile(creds_file.read(),
                                      include=include_profiles,
                                      exclude=exclude_profiles)
        self._template = Template(cfn_template_path)

    @property
    def profiles(self):
        return self._creds.profiles

    @property
    def template(self):
        return self._template.body

    def create_stacks(self, confirm=True):
        if confirm:
            print(
                "The following accounts will be provisioned: \n\n{}".format(
                    '\n'.join(self.profiles))
            )
            proceed = input("\nProceed? [Y]/N ") or "Y"
            print(proceed.upper())
            if proceed.upper() != "Y" and proceed.upper() != "YES":
                sys.exit()





