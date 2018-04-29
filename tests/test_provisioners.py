import moto
import pytest

from lib.provisioners import AwsProvisioner
from tests import VALID_TEMPLATE1_URL

TEST_PARAMS = [
    {},
    {'AwsAccountLinking': 'true', 'OcmsExternalId': 'test123'}
]


# Used to use different cfn_params in the test see
# https://hackebrot.github.io/pytest-tricks/create_tests_via_parametrization/
# for more details
@pytest.fixture(params=TEST_PARAMS)
def cfn_params(request):
    return request.param


@moto.mock_sts
@moto.mock_cloudformation
def test_provision_accounts(cfn_params):
    """Create stack with different params"""
    test_region = 'us-east-1'
    test_stack_name = 'test-stack'
    test_profiles = ['profile-include1']
    provisioner = AwsProvisioner(
                                    VALID_TEMPLATE1_URL,
                                    test_region,
                                    test_stack_name,
                                    cfn_params,
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

    assert stack_status == ['CREATE_COMPLETE']

