from aws_cdk import (
    core,
    aws_ec2,
    aws_iam
)


class EC2StackWithRoles(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #import vpc info
        vpc = aws_ec2.Vpc.from_lookup(
            self,
            "vpc",
            vpc_id="vpc-1f39b977"
        )

        #import user-data scripts
        with open("userdata_scripts/setup.sh", mode="r") as file:
            user_data = file.read()

        #get latest ami from any region
        aws_linux_ami = aws_ec2.MachineImage.latest_amazon_linux(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            storage=aws_ec2.AmazonLinuxStorage.EBS,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM
        )

        #ec2
        test_server = aws_ec2.Instance(
            self,
            "ec2id",
            instance_type=aws_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="TestServer01",
            machine_image=aws_linux_ami,
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC
            ),
            key_name="SAA-C01",
            user_data=aws_ec2.UserData.custom(user_data)
        )

        #add custom ebs for ec2
        test_server.instance.add_property_override(
            "BlockDeviceMappings", [
                {
                    "DeviceName": "/dev/sdb",
                    "Ebs": {
                        "VolumeSize": "10",
                        "VolumeType": "io1",
                        "Iops": "100",
                        "DeleteOnTermination": "true"
                    }
                }
            ]
        )

        #allow web traffic
        test_server.connections.allow_from_any_ipv4(
            aws_ec2.Port.tcp(80),
            description="allow web traffic"
        )

        # add permission to instances profile
        test_server.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )
        test_server.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )
        )

        output_server_ip = core.CfnOutput(
            self,
            "serverip01",
            description="test server ip",
            value=test_server.instance_public_ip
        )