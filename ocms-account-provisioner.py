#!/usr/bin/env python3
import argparse
import logging
import os
from pathlib import Path

from lib.provisioners import AwsProvisioner


##########################################################################
# Args

parser = argparse.ArgumentParser(
    description="Provisions AWS accounts to be used with the OCMS. Use the "
                "AWS_SHARED_CREDENTIALS_FILE env var to change the desired "
                "AWS credentials file."
)

parser.add_argument('--cfn-template-url',
                    default='file://bct-ocms-iam.yaml',
                    help="s3 or file url to cloudformation template."
                    )
parser.add_argument('--aws-region',
                    default="us-east-1",
                    help="aws region used for cfn stack."
                    )
parser.add_argument('--cfn-stack-name',
                    default='bct-ocms-iam',
                    help="Name of cfn stack."
                    )
parser.add_argument('--aws-include-profiles',
                    default=None,
                    help="comma separated list or regex of profiles that "
                         "should be provisioned"
                    )
parser.add_argument('--aws-exclude-profiles',
                    default=None,
                    help="comma separated list or regex of profiles that "
                         "should not be provisioned."
                    )
parser.add_argument('--no-confirm',
                    action='store_true',
                    help="Does not confirm the profiles that will be "
                         "confirmed prior to the provisioning them."
                    )
parser.add_argument('--log-level',
                    default='warn',
                    help="Log level sent to the console.")

args = parser.parse_args()

##########################################################################


def list_or_str(text):
    """returns either a list or string based on if text is comma separated"""

    if text is None:
        return None
    elif "," in text:
        return text.split(",")
    else:
        return text


if __name__ == '__main__':
    logging_levels = {
        'debug':    logging.DEBUG,
        'info':     logging.INFO,
        'warn':     logging.WARN,
        'error':    logging.ERROR
    }
    log_level = logging_levels[args.log_level.lower()]

    logger = logging.getLogger('lib')
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    if not (args.cfn_template_url.startswith("s3://")
            or args.cfn_template_url.startswith("file://")):
        raise ValueError(
            "cfn_template_url must start with s3:// or file://"
        )

    aws_provisioner = AwsProvisioner(
                                         args.cfn_template_url,
                                         args.aws_region,
                                         args.cfn_stack_name,
                                         include_profiles=list_or_str(
                                             args.aws_include_profiles
                                         ),
                                         exclude_profiles=list_or_str(
                                             args.aws_exclude_profiles
                                         )
                                     )

    aws_provisioner.provision_accounts(confirm=not args.no_confirm)
