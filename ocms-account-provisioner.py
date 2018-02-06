#!/usr/bin/env python3
import argparse
import json
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
                    help="s3 or file url to cloudformation template."
                    )
parser.add_argument('--AwsRegion',
                    help="aws region used for cfn stack."
                    )
parser.add_argument('--CfnStackName',
                    help="Name of cfn stack."
                    )
parser.add_argument('--CfnParams',
                    help="JSON object of CFN Params."
                    )
parser.add_argument('--IncludeProfiles',
                    help="comma separated list or regex of profiles that "
                         "should be provisioned"
                    )
parser.add_argument('--ExcludeProfiles',
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


def build_config(config_dict, args_dict):
    """Returns dict based on dict of config file contents and dict of args"""

    # Set defaults
    config = {
                'CfnTemplateUrl': 'file://bct-ocms-iam.yaml',
                'AwsRegion': 'us-east-1',
                'CfnStackName': 'bct-ocms-iam',
    }

    args_with_values = {
        key: value for (key, value) in args_dict.items() if value is not None
    }

    config.update(config_dict)
    config.update(args_with_values)

    if not (config['CfnTemplateUrl'].startswith("s3://")
            or config['CfnTemplateUrl'].startswith("file://")):
        raise ValueError(
            "CfnTemplateUrl must start with s3:// or file://"
        )

    for key, value in config.items():
        if type(value) is str:
            try:
                config[key] = dict(json.loads(value))
                break
            except ValueError:
                pass

        if type(value) is str and ',' in value:
            config[key] = value.split(',')

    return config


def provision_accounts(config):
    """Provisions AWS Accounts"""
    
    aws_provisioner = AwsProvisioner(
                                 config['CfnTemplateUrl'],
                                 config['AwsRegion'],
                                 config['CfnStackName'],
                                 config['CfnParams'],
                                 include_profiles=config['IncludeProfiles'],
                                 exclude_profiles=config['ExcludeProfiles']
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

    with open(args.ConfigFile) as config_file:
        provision_config = build_config(
                                        yaml.load(config_file.read()),
                                        vars(args)
                            )

    print(provision_config)
    print(type(provision_config['CfnParams']))
    #provision_accounts(provision_config)



