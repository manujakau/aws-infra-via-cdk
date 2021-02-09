from aws_cdk import (
    core,
    aws_ec2,
    aws_iam,
    aws_lambda,
    aws_sns,
    aws_sns_subscriptions as aws_sns_subc,
    aws_cloudwatch as aws_cw,
    aws_cloudwatch_actions as aws_cw_ats
)


class MonitoringStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #sns topic for monitor
        snstopic_monitor01 = aws_sns.Topic(
            self,
            "MonitorSnsTopic",
            display_name="monitor webapp",
            topic_name="EC2Monitor"
        )

        #add subcriptions  to sns
        snstopic_monitor01.add_subscription(
            aws_sns_subc.EmailSubscription("mail@manuja.me")
        )

        ## vpc block ##
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
        ## end vpc block ##

        ## ec2 block ##
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
            vpc=custom_vpc,
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
        ## end ec2 block ##

        ## lambda block ##
                #import function code
        try:
            with open("serverless_stack/functions/function.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')

        #function
        function_01 = aws_lambda.Function(
            self,
            "lambdafunction01",
            function_name="LambdaTestCDK",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                'LOG_LEVEL': 'INFO',
                'AUTOMATION': 'SKON'
            }
        )
        ## end lambda block ##

        ## monitor block ##
        #ec2 metric for cpu usage
        ec2_metric_01 = aws_cw.Metric(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",
            dimensions={
                "InstanceID": test_server.instance_id
            },
            period=core.Duration.minutes(5)
        )

        #under utilize alram ec2
        low_cpu_ec2 = aws_cw.Alarm(
            self,
            "lowcpualram",
            alarm_description="low cpu utilization",
            alarm_name="Low-CPU-Alarm",
            actions_enabled=True,
            metric=ec2_metric_01,
            threshold=10,
            comparison_operator=aws_cw.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(5),
            treat_missing_data=aws_cw.TreatMissingData.NOT_BREACHING
        )

        #sns on ec2 alram
        low_cpu_ec2.add_alarm_action(
            aws_cw_ats.SnsAction(
                snstopic_monitor01
            )
        )

        #Lambda alram
        function_01_alarm = aws_cw.Alarm(
            self,
            "LambdaAlarm",
            metric=function_01.metric_errors(),
            threshold=2,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(5)
        )

        #sns on lambda alarm
        function_01_alarm.add_alarm_action(
            aws_cw_ats.SnsAction(
                snstopic_monitor01
            )
        )