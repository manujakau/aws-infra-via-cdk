from aws_cdk import (
    core,
    aws_ec2,
    aws_iam,
    aws_elasticloadbalancingv2 as aws_elbv2,
    aws_autoscaling as aws_asg
)


class WebAppInfraStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #import user-data scripts
        try:
            with open("userdata_scripts/setup.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print('Userdata can not apply')
    
        #get latest ami from any region
        aws_linux_ami = aws_ec2.MachineImage.latest_amazon_linux(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            storage=aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM
        )

        #application ELB
        alb = aws_elbv2.ApplicationLoadBalancer(
            self,
            "WebAlbID",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerALB"
        )

        #ELB security groups
        alb.connections.allow_from_any_ipv4(
            aws_ec2.Port.tcp(80),
            description="Allow web traffic to ALB over port 80"
        )

        #ELB listener
        listener = alb.add_listener(
            "AlbListenerID",
            port=80,
            open=True
        )

        #App Server IAM roles
        web_app_role = aws_iam.Role(
            self,
            "WebAppRoleID",
            assumed_by=aws_iam.ServicePrincipal(
                'ec2.amazonaws.com'
            ),
            managed_policies= [
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonSSMManagedInstanceCore'
                ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonS3ReadOnlyAccess'
                )   
            ]
        )

        #Launch Configuration and AutoScaling
        web_app_lc_asg = aws_asg.AutoScalingGroup(
            self,
            "WebAppLcAsgID",
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PRIVATE
            ),
            instance_type=aws_ec2.InstanceType(
                instance_type_identifier="t2.micro"
            ),
            machine_image=aws_linux_ami,
            role=web_app_role,
            min_capacity=2,
            max_capacity=3,
            desired_capacity=2,
            user_data=aws_ec2.UserData.custom(user_data)
        )

        #Allow asg security group to recive trafic from alb
        web_app_lc_asg.connections.allow_from(
            alb, 
            aws_ec2.Port.tcp(80),
            description="Allow asg to traffic from alb"
        )

        #Add asg to alb target group
        listener.add_targets(
            "AlbListenerID",
            port=80,
            targets=[web_app_lc_asg]
        )

        #alb url output
        alb_output = core.CfnOutput(
            self,
            "AlbUrl",
            value=alb.load_balancer_dns_name,
            description="Web App Url"
        )