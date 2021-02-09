from aws_cdk import (
    core,
    aws_ssm,
    aws_iam,
    aws_secretsmanager as aws_secrm
)

class IAMStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #ssm parameter for test
        ssm_01 = aws_ssm.StringParameter(
            self,
            "ssm_01",
            description="test parameter",
            parameter_name="/test/demo/iam",
            string_value="123",
            tier=aws_ssm.ParameterTier.STANDARD
        )

        #IAM users and Groups
        user01_password = aws_secrm.Secret(
            self,
            "user01password",
            description="User01 Password",
            secret_name="user01_password"
        )

        #users
        user01 = aws_iam.User(
            self,
            "user01",
            password=user01_password.secret_value,
            user_name="user01"
        )

        user02 = aws_iam.User(
            self,
            "user02",
            password=core.SecretValue.plain_text(
                "Testpassowrd123"
            ),
            user_name="user02"
        )

        #iam group
        test_group = aws_iam.Group(
            self,
            "test_group",
            group_name="test-group"
        )
        test_group.add_user(
            user02
        )

        #iam policy
        test_group.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )
        )

        #grant ssm parameter access to iam group
        ssm_01.grant_read(
            test_group
        )

        #grant test group to list all parameters in aws console
        test_group_stemt = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ssm:DescribeParameters"
            ]
        )
        test_group_stemt.sid="ListAllParametersForTestGroup"

        #add PolicyStatement to group
        test_group.add_to_policy(
            test_group_stemt
        )

        #iam role
        test_role = aws_iam.Role(
            self,
            "test_role",
            assumed_by=aws_iam.AccountPrincipal(f"{core.Aws.ACCOUNT_ID}"),
            role_name="cdk_test_role"
        )

        #policy attached to role
        managed_policy_01 = aws_iam.ManagedPolicy(
            self,
            "managed_policy_01_list_ec2",
            description="list ec2",
            managed_policy_name="managed_policy_01_list_ec2",
            statements=[
                aws_iam.PolicyStatement(
                    effect=aws_iam.Effect.ALLOW,
                    actions=[
                        "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "cloudwatch:Get*"
                    ],
                    resources=["*"]
                )
            ],
            roles=[
                test_role
            ]
        )


        #login url
        login_output01 = core.CfnOutput(
            self,
            "login_output01",
            description="Login URL for user02",
            value=f"https://{core.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
        )