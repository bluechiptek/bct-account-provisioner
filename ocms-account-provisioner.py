#!/usr/bin/env python3
import argparse
import logging
import pathlib

from lib.provisioners import AwsProvisioner


##########################################################################
# Args

parser = argparse.ArgumentParser(
    description="Provisions AWS accounts to be used with the OCMS."
)

parser.add_argument('--aws-creds-file',
                    default=str(pathlib.Path.home()) + "/.aws/credentials",
                    help="Path to non-default aws credentials file."
                    )
parser.add_argument('--cfn-template-url',
                    default='s3://bct-public-templates/ocms/ocms_iam_stack.yaml',
                    help="s3 or file url to cloudformation template."
                    )
parser.add_argument('--aws-region',
                    default="us-east-1",
                    help="aws region used for cfn stack."
                    )
parser.add_argument('--cfn-stack-name',
                    default='BCT-OC-CostMgmt-IAM',
                    help="Name of cfn stack."
                    )
parser.add_argument('--aws-include-profiles',
                    default=None,
                    help="list or regex of profiles that should be provisioned"
                    )
parser.add_argument('--aws-exclude-profiles',
                    default=None,
                    help="list or regex of profiles that should not be "
                          "provisioned."
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

    aws_provisioner = AwsProvisioner(args.aws_creds_file,
                                     args.cfn_template_url,
                                     args.aws_region,
                                     args.cfn_stack_name,
                                     include_profiles=args.aws_include_profiles,
                                     exclude_profiles=args.aws_exclude_profiles
                                     )

    aws_provisioner.provision_accounts(confirm=not args.no_confirm)
