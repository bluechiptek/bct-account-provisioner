import botocore
import moto
import pytest

from provisioner.stacks import Stack, Template


def test_template_invalid_path_format():
    with pytest.raises(ValueError):
        Template("test")


def test_template_invalid_file():
    with pytest.raises(RuntimeError):
        Template('file://provisioner/tests/cfn_test_invalid_template.yaml')


def test_template_hexdigest():
    """hexdigest test reading from file and validating template"""
    template = Template('file://provisioner/tests/cfn_test_template1.yaml')
    assert template.hexdigest == 'e52c979111e5ea905648146555c689b32b2d5bea'

