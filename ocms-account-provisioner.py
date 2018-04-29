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


parser.add_argument('--config-file',
                    dest='ConfigFile',
                    default='config.yaml',
                    help="Path to provisioner config file. "
                         "Defaults to config.yaml"
                    )
parser.add_argument('--template-url',
                    dest='CfnTemplateUrl',
                    required=True,
                    help="s3 or file url to cloudformation template. "
                    )
parser.add_argument('--region',
                    dest='AwsRegion',
                    help="aws region used for cfn stack. "
                         "Defaults to us-east-1"
                    )
parser.add_argument('--stack-name',
                    dest='CfnStackName',
                    help="Name of cfn stack. "
                         "Defaults to name of the template file "
                         "(i.e. BctOcms.yaml becomes BctOcms) "
                    )
parser.add_argument('--cfn-params',
                    dest='CfnParams',
                    help="JSON object of CFN Params."
                    )
parser.add_argument('--include-profiles',
                    dest='IncludeProfiles',
                    help="comma separated list or regex of profiles that "
                         "should be provisioned"
                    )
parser.add_argument('--exclude-profiles',
                    dest='ExcludeProfiles',
                    help="comma separated list or regex of profiles that "
                         "should not be provisioned."
                    )
parser.add_argument('--no-confirm',
                    dest='NoConfirm',
                    action='store_true',
                    help="Does not confirm the profiles that will be "
                         "confirmed prior to the provisioning them."
                    )
parser.add_argument('--log-level',
                    dest='LogLevel',
                    default='warn',
                    help="Log level sent to the console.")

args = parser.parse_args()

##########################################################################


def build_config(config_dict, args_dict):
    """Returns dict based on dict of config file contents and dict of args"""

    # Set defaults
    config = {
                'AwsRegion': 'us-east-1'
    }

    args_with_values = {
        key: value for key, value in args_dict.items() if value is not None
    }

    # If arg is a string then check to see if the arg is JSON and if so then
    # deserialize it. If it can not be deserialized, then see if it can be
    # split into a list.
    for key, value in args_with_values.items():
        if type(value) is str:
            try:
                args_with_values[key] = dict(json.loads(value))
                logger.debug("Deserialized JSON into dict: {}".format(value))
                break
            except ValueError:
                pass

        if type(value) is str and ',' in value:
            args_with_values[key] = value.split(',')
            logger.debug("Split string into list: {}".format(value))

    # Check to see if any JSON has been deserialized into a dict. If so,
    # then either update an existing k:v in config_dict or create a new k:v
    for key, value in args_with_values.items():
        if type(value) is dict and config_dict.get(key):
            config_dict[key].update(args_with_values[key])
        else:
            config_dict[key] = args_with_values[key]

    config.update(config_dict)

    if (not config.get('CfnTemplateUrl')
        or not (config['CfnTemplateUrl'].startswith("s3://")
           or config['CfnTemplateUrl'].startswith("file://"))):
                raise ValueError(
                    "CfnTemplateUrl must start with s3:// or file://"
                )

    # Set stack name based on template file
    if not config.get('CfnStackName'):
        path_parts = config['CfnTemplateUrl'].split('/')
        filename_parts = path_parts[-1].split('.')
        if filename_parts[-1].lower() not in ['json', 'template',
                                              'yaml', 'yml']:
            raise ValueError(
                "CfnTemplateUrl must end with json, template , yaml or yml"
            )

        config['CfnStackName'] = filename_parts[-2]

    logger.debug("config dict: {}".format(config))
    return config


def provision_accounts(config):
    """Provisions AWS Accounts"""
    
    aws_provisioner = AwsProvisioner(
                             config['CfnTemplateUrl'],
                             config['AwsRegion'],
                             config['CfnStackName'],
                             config.get('CfnParams', {}),
                             include_profiles=config.get('IncludeProfiles'),
                             exclude_profiles=config.get('ExcludeProfiles')
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

    if Path(args.ConfigFile).exists():
        with open(args.ConfigFile) as config_file:
            config_dict = yaml.load(config_file.read())
    else:
        logger.debug(
            "{} not found, so just using CLI args".format(args.ConfigFile)
        )
        config_dict = {}

    provision_config = build_config(config_dict, vars(args))

    provision_accounts(provision_config)



