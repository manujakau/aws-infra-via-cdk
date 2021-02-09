from aws_cdk import (
    core,
    aws_ec2
)


class WebAppVPCStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_config = self.node.try_get_context('envs')['prod']

        self.custom_vpc = aws_ec2.Vpc(
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
        core.Tags.of(self.custom_vpc).add("Owner", "Admin")

        core.CfnOutput(
            self,
            "CustomVpcIDoutput",
            value=self.custom_vpc.vpc_id,
            export_name="CustomVPCid"
        )