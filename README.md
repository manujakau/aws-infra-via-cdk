
# CDK Python project!

To manually create a virtualenv on Debian/Ubuntu:

prerequisite
```
$ sudo apt install -y python3-pip
$ sudo apt install -y python3-venv
$ curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
$ sudo apt update -y
$ sudo apt-get install -y nodejs
$ sudo apt-get install -y build-essential
$ sudo npm install -g aws-cdk
```

Setup CDK project
```
$ git clone git@github.com:manujakau/aws-cdk-infra-01.git
```

Then follow the below steps to complete rest.
```
$ mkdir <project name> && cd <project name>
$ cdk init
$ cdk init --language python
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk bootstrap
$ cdk ls
$ cdk synth
```

After bootstrap modify cdk.json as below example if looking forward to use variables.
```
{
  "app": "python3 app.py",
  "versionReporting": false,
  "context": {
    "@aws-cdk/core:enableStackNameDuplicates": "true",
    "aws-cdk:enableDiffNoFail": "true",
    "@aws-cdk/core:stackRelativeExports": "true",
    "@aws-cdk/aws-ecr-assets:dockerIgnoreSupport": true,
    "@aws-cdk/aws-secretsmanager:parseOwnedSecretName": true,
    "@aws-cdk/aws-kms:defaultKeyPolicies": true,
    "envs": {
      "dev": {
        "region": "us-east-1"
      },
      "prod": {
        "support_email": "test@admin.com",
        "region": "eu-central-1",
        "aws_account_id": "<your aws account id>",
        "encryption": true,
        "kms_arn": "arn:aws:kms:eu-central-1:<your aws account id>:key/<arn value>",
        "vpc_config": {
          "vpc_cidr": "10.192.0.0/16",
          "cidr_mask": 24,
          "set_reserve": false
        }
      },
      "default": {
        "region": "eu-central-1",
        "aws_account_id": "<your aws account id>",
        "ami_id": "ami-03c3a7e4263fd998c"
      }
    }
  }
}
```

In setup.py edit below block to mtach current cdk version installed to the system.
```
    install_requires=[
        "aws-cdk.core==1.88.0",
    ]
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
