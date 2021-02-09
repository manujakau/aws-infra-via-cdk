from aws_cdk import (
    core,
    aws_ssm,
    aws_secretsmanager as aws_secrm
)

import json

class SSMStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #SSM parameters
        ssm01 = aws_ssm.StringParameter(
            self,
            "ssmparameter01",
            description="Test Config",
            parameter_name="ConcurrentUsers",
            string_value="100",
            tier=aws_ssm.ParameterTier.STANDARD
        )

        secret01 = aws_secrm.Secret(
            self,
            "secret01",
            description="DB password",
            secret_name="db_password"
        )

        secret_templet01 = aws_secrm.Secret(
            self,
            "secret_templet01",
            description="templatized user credentials",
            secret_name="user_db_auth",
            generate_secret_string=aws_secrm.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {
                        "username": "Admin"
                    }
                ),
                generate_string_key="password"
            )
        )

        output_ssm01 = core.CfnOutput(
            self,
            "output_ssm01",
            description="ConcurrentUsersCount",
            value=ssm01.string_value
        )

        output_secret01 = core.CfnOutput(
            self,
            "output_secret01",
            description="DB Password-secret01",
            value=f"{secret01.secret_value}"
        )