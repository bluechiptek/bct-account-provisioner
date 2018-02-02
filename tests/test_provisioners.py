import moto

from lib.provisioners import AwsProvisioner
from tests import VALID_TEMPLATE1_URL


@moto.mock_sts
@moto.mock_cloudformation
def test_provision_accounts():
    test_region = "us-east-1"
    test_stack_name = "test-stack"
    test_profiles = ['profile-include1', 'profile-include2']
    provisioner = AwsProvisioner(
                                    VALID_TEMPLATE1_URL,
                                    test_region,
                                    test_stack_name,
                                    include_profiles=test_profiles
                                )

    provisioner.provision_accounts(confirm=False)
    stack_status = []
    for account in provisioner.accounts:
        cfn = account.session.client('cloudformation',
                                     region_name=test_region)
        response = cfn.describe_stacks(StackName=test_stack_name)
        status = response['Stacks'][0]['StackStatus']
        stack_status.append(status)
    assert stack_status == ['CREATE_COMPLETE', 'CREATE_COMPLETE']

