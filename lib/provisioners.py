import logging
import sys

from lib.accounts import AwsCredsFile, AwsAccount
from lib.stacks import Stack, Template

logger = logging.getLogger(__name__)


class AwsProvisioner():

    def __init__(self,
                 creds_file_path,
                 cfn_template_path,
                 region,
                 stack_name,
                 include_profiles=None,
                 exclude_profiles=None):
        with open(creds_file_path) as creds_file:
            self._creds = AwsCredsFile(creds_file.read(),
                                      include=include_profiles,
                                      exclude=exclude_profiles)
        self._region = region
        self._stack_name = stack_name
        self._template = Template(cfn_template_path)
        self._accounts = [AwsAccount(profile)
                          for profile in self._creds.profiles]

    @property
    def profiles(self):
        return self._creds.profiles

    @property
    def template(self):
        return self._template.body

    def provision_accounts(self, confirm=True):
        if confirm:
            account_id_names = []
            for account in self._accounts:
                id_name = "{} ({})".format(account.id, account.profile_name)
                account_id_names.append(id_name)
            print(
                "The following accounts will be provisioned: \n\n{}".format(
                    '\n'.join(account_id_names))
            )
            proceed = input("\nProceed? [Y]/N ") or "Y"
            if proceed.upper() != "Y" and proceed.upper() != "YES":
                sys.exit()
        for account in self._accounts:
            cfn = account.session.client('cloudformation',
                                         region_name=self._region)
            logger.info("Provisioning account {} ({})".format(
                account.id, account.profile_name
            ))
            stack = Stack(self._stack_name, cfn_client=cfn)
            stack.apply_template(self._template.body)







