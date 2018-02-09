# OCMS-ACCOUNT-PROVISIONER

The ocms-account-provisioner, referred to as just the provisioner, is a utility that can automate connecting your AWS accounts with the various services used to deliver an OptimizedCloud Blueprint. Connectivity from these various services is done by creating a CloudFormation stack in each of your desired AWS accounts with the neccisary roles and permissions.

This software is distributed under the GNU General Public License v3.0. Please see the file LICENSE.txt for terms of use and redistribution.

## DESCRIPTION

The provisioner facilities the creation of these CloudFormation stacks. It does this by discovering profiles via an AWS CLI credentials file and then creating the CloudFormation stacks in those accounts.

## INSTALLATION

ocms-account-provisioner is written in Python3.

ocms-account-provisioner requires aws cli to be installed. A requirements.txt has been provided which includes other packages needed to run tests.

## CONFIGURATION

By default the provisioner will read the default AWS CLI credentials file (~/aws/credentials), but a different credentials file can be used by setting the AWS_SHARED_CREDENTIALS_FILE environment variable . Additionally, the provisioner allows for you to only include or specifically exclude discovered profiles via CLI arguments.

The provisioner is configured either via CLI arguments or via a config.yaml file. Typically the BlueChipTek cloud services engineering working on your Blueprint implementation will provide you a config.yaml file. This config.yaml file will contain details that need to be provided by BlueChipTek, such as values for the CloudFormation parameters.

CLI arguments are as follows, but can also be viewed with the `--help` argument (and should be in case this README hasn't been updated).

```
  --ConfigFile CONFIGFILE
                        Path to provisioner config file. Defaults to
                        config.yaml
  --CfnTemplateUrl CFNTEMPLATEURL
                        s3 or file url to cloudformation template. Defaults to
                        file://bct-ocms-iam.yaml
  --AwsRegion AWSREGION
                        aws region used for cfn stack. Defaults to us-east-1
  --CfnStackName CFNSTACKNAME
                        Name of cfn stack. Defaults to bct-ocms-iam
  --CfnParams CFNPARAMS
                        JSON object of CFN Params.
  --IncludeProfiles INCLUDEPROFILES
                        comma separated list or regex of profiles that should
                        be provisioned
  --ExcludeProfiles EXCLUDEPROFILES
                        comma separated list or regex of profiles that should
                        not be provisioned.
  --NoConfirm           Does not confirm the profiles that will be confirmed
                        prior to the provisioning them.
  --LogLevel LOGLEVEL   Log level sent to the console.

```

By default the config.yaml is expected to be located at ./config.yaml. You can specify any argument via the config.yaml or via a CLI argument. The CLI argument will override any config option set in the config.yaml. A sample config.yaml setting the CfnParams can be found at ./test/config.yaml.

## USAGE

To run the provisioner you will need to provide it with the values needed for the CloudFormation Parameters. This is typically done via a config.yaml file provided by BlueChipTek, but can be done via `--CfnParams` CLI argument. Defaults are set for all other arguments.












