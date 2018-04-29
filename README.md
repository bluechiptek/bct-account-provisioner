# OCMS-ACCOUNT-PROVISIONER

The ocms-account-provisioner, referred to as just the provisioner, is a utility that can automate connecting your AWS accounts with the various services used to deliver an OptimizedCloud service. Connectivity from these various services is done by creating a CloudFormation stack in each of your desired AWS accounts with the necessary roles and permissions.

This software is distributed under the GNU General Public License v3.0. Please see the file LICENSE.txt for terms of use and redistribution.

## DESCRIPTION

The provisioner facilitates the creation of CloudFormation stacks. It does this by discovering profiles via an AWS CLI credentials file and then creating CloudFormation stacks in those accounts.

## INSTALLATION

ocms-account-provisioner is written in Python3.

ocms-account-provisioner requires aws cli to be installed. A requirements.txt has been provided which includes other packages needed to run tests.

## CONFIGURATION

By default the provisioner will read the default AWS CLI credentials file (~/aws/credentials), but a different credentials file can be used by setting the `AWS_SHARED_CREDENTIALS_FILE` environment variable . Additionally, the provisioner allows for you to include or  exclude discovered profiles via CLI arguments.

The provisioner is configured either via CLI arguments, a config.yaml file or some combination. Typically the BlueChipTek cloud services engineering working on your service implementation will provide you a config.yaml file. This config.yaml file will contain details that need to be provided by BlueChipTek, such as External IDs.

CLI arguments are as follows, but can also be viewed with the `--help` argument (and should be in case this README hasn't been updated).

```
  --config-file CONFIGFILE
                        Path to provisioner config file. Defaults to
                        config.yaml
  --template-url CFNTEMPLATEURL
                        s3 or file url to cloudformation template.
  --region AWSREGION    aws region used for cfn stack. Defaults to us-east-1
  --stack-name CFNSTACKNAME
                        Name of cfn stack. Defaults to name of the template
                        file (i.e. BctOcms.yaml becomes BctOcms)
  --cfn-params CFNPARAMS
                        JSON object of CFN Params.
  --include-profiles INCLUDEPROFILES
                        comma separated list or regex of profiles that should
                        be provisioned
  --exclude-profiles EXCLUDEPROFILES
                        comma separated list or regex of profiles that should
                        not be provisioned.
  --no-confirm          Does not confirm the profiles that will be confirmed
                        prior to the provisioning them.
  --log-level LOGLEVEL  Log level sent to the console.

```

By default the config.yaml is expected to be located at ./config.yaml. You can specify any argument via the config.yaml or via a CLI argument. The CLI argument will override any config option set in the config.yaml. A sample config.yaml setting the CfnParams can be found at ./test/config.yaml.

## USAGE

To run the provisioner you will need to provide it with the URL for the CloudFormation template and values needed the templates's parameters.

The CloudFormation template URL is provided via the `--template-url` CLI argument. The URL must be provided in **file://** or **s3://** format.

Parameters for the CloudFormation template are typically provided by both a config.yaml file and via `--cfn-params` CLI argument. BlueChipTek will provide a config.yaml and you will provide additional arguments via the CLI as directed by BlueChipTek.

Defaults are set for all other arguments.

The `--include-profiles` and `--exclude-profiles` can be used to select the profiles used in your AWS credentials file for account discovery. These parameters take either RegEx (not generic globing) or a comma separate list (no spaces between list items). By default the provisioner will prompt you to approve the list of accounts that it will provision.

The profiles used for account discovery should have the necessary permissions to create a CloudFormation Stack.

In the following example assume the following profiles are defined in the credentials file: include-profile1, include-profile2, exclude-profile1 & exclude-profile2.

Use RegEx to only select profiles that start with *include*
```
./ocms-account-provisioner.py --config-file tests/config.yaml --include-profiles include.*
The following accounts will be provisioned:

679806829XYZ (include-profile1)
000925560XYZ (include-profile2)

Proceed? [Y]/N
```

Use a list to only select profiles *include-profile1* and *include-profile2*.
```
./ocms-account-provisioner.py --config-file tests/config.yaml --include-profiles include-profile1,include-profile2
The following accounts will be provisioned:

679806829XYZ (include-profile1)
000925560XYZ (include-profile2)

Proceed? [Y]/N
```

Use RegEx to only select profiles that contain the work *profile*, but exclude *exclude-profile1* and *exclude-profile2* via a list.
```
./ocms-account-provisioner.py --config-file tests/config.yaml --exclude-profiles .*profile.* --exclude-profiles exclude-profile1,exclude-profile2
The following accounts will be provisioned:

679806829XYZ (include-profile1)
000925560XYZ (include-profile2)

Proceed? [Y]/N
```
