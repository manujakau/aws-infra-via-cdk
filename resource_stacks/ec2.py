from aws_cdk import (
    core,
    aws_ec2
)


class EC2Stack(core.Stack):

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

        #ec2
        test_server = aws_ec2.Instance(
            self,
            "ec2id",
            instance_type=aws_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="TestServer01",
            machine_image=aws_ec2.MachineImage.generic_linux(ami_map=
                {
                    "eu-central-1": "ami-03c3a7e4263fd998c"
                }
            ),
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC
            ),
            key_name="SAA-C01",
            user_data=aws_ec2.UserData.custom(user_data)
        )

        #allow web traffic
        test_server.connections.allow_from_any_ipv4(
            aws_ec2.Port.tcp(80),
            description="allow web traffic"
        )

        output_server_ip = core.CfnOutput(
            self,
            "serverip01",
            description="test server ip",
            value=test_server.instance_public_ip
        )