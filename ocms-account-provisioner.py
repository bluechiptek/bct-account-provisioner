#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path
import yaml

from lib.provisioners import AwsProvisioner


##########################################################################
# Args

parser = argparse.ArgumentParser(
    description="Provisions AWS accounts to be used with the OCMS. Use the "
                "AWS_SHARED_CREDENTIALS_FILE env var to change the desired "
                "AWS credentials file."
)


parser.add_argument('--ConfigFile',
                    default='config.yaml',
                    help="Path to provisioner config file"
                    )
parser.add_argument('--CfnTemplateUrl',
                    default='file://bct-ocms-iam.yaml',
                    help="s3 or file url to cloudformation template."
                    )
parser.add_argument('--AwsRegion',
                    default="us-east-1",
                    help="aws region used for cfn stack."
                    )
parser.add_argument('--CfnStackName',
                    default='bct-ocms-iam',
                    help="Name of cfn stack."
                    )
parser.add_argument('--IncludeProfiles',
                    default=None,
                    help="comma separated list or regex of profiles that "
                         "should be provisioned"
                    )
parser.add_argument('--ExcludeProfiles',
                    default=None,
                    help="comma separated list or regex of profiles that "
                         "should not be provisioned."
                    )
parser.add_argument('--NoConfirm',
                    action='store_true',
                    help="Does not confirm the profiles that will be "
                         "confirmed prior to the provisioning them."
                    )
parser.add_argument('--LogLevel',
                    default='warn',
                    help="Log level sent to the console.")

args = parser.parse_args()

##########################################################################


def list_or_str(text):
    """Returns either a list or string based on if text is comma separated"""

    if text is None:
        return None
    elif "," in text:
        return text.split(",")
    else:
        return text


def build_config(config_yaml, args):
    """Returns dict based on config yaml and args"""
    config_dict = args.copy()
    config_dict.update(yaml.load(config_yaml))
    return config_dict


def provision_accounts(config):
    """Provisions AWS Accounts"""
    
    aws_provisioner = AwsProvisioner(
                                         config['CfnTemplateUrl'],
                                         config['AwsRegion'],
                                         config['CfnStackName'],
                                         include_profiles=list_or_str(
                                             config['IncludeProfiles']
                                         ),
                                         exclude_profiles=list_or_str(
                                             config['ExcludeProfiles']
                                         )
                                     )

    aws_provisioner.provision_accounts(confirm=not config['NoConfirm'])


if __name__ == '__main__':
    logging_levels = {
        'debug':    logging.DEBUG,
        'info':     logging.INFO,
        'warn':     logging.WARN,
        'error':    logging.ERROR
    }
    log_level = logging_levels[args.LogLevel.lower()]

    logger = logging.getLogger('lib')
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    if not Path(args.ConfigFile).exists():
        raise ValueError(
            "Unable to access config file: {}".format(args.ConfigFile)
        )

    if not (args.CfnTemplateUrl.startswith("s3://")
            or args.CfnTemplateUrl.startswith("file://")):
        raise ValueError(
            "cfn_template_url must start with s3:// or file://"
        )

    with open(args.ConfigFile) as config_file:
        config = build_config(config_file.read(), vars(args))

    provision_accounts(config)


