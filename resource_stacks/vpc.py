from aws_cdk import (
    core,
    aws_ec2
)


class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_config = self.node.try_get_context('envs')['prod']

        custom_vpc = aws_ec2.Vpc(
            self,
            "CustomVpcID",
            cidr=prod_config['vpc_config']['vpc_cidr'],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name="PublicSubnet", cidr_mask=prod_config['vpc_config']['cidr_mask'], subnet_type=aws_ec2.SubnetType.PUBLIC
                ),
                aws_ec2.SubnetConfiguration(
                    name="PrivateSubnet", cidr_mask=prod_config['vpc_config']['cidr_mask'], subnet_type=aws_ec2.SubnetType.PRIVATE
                ),
                aws_ec2.SubnetConfiguration(
                    name="DbSubnet", cidr_mask=prod_config['vpc_config']['cidr_mask'], subnet_type=aws_ec2.SubnetType.ISOLATED
                )
            ]
        )

        #simple tagging
        core.Tags.of(custom_vpc).add("Owner", "Admin")

        core.CfnOutput(
            self,
            "CustomVpcIDoutput",
            value=custom_vpc.vpc_id,
            export_name="CustomVPCid"
        )

        #import and use exsisting resources
        import_vpc = aws_ec2.Vpc.from_lookup(
            self,
            "importedvpc",
            vpc_id="vpc-1f39b977"
        )

        core.CfnOutput(
            self,
            "import_vpc_output",
            value=import_vpc.vpc_id
        )

        #peer default vpc with custom vpc
        peer_vpc = aws_ec2.CfnVPCPeeringConnection(
            self,
            "peervpc",
            peer_vpc_id=custom_vpc.vpc_id,
            vpc_id=import_vpc.vpc_id
        )