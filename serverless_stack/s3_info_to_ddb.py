from aws_cdk import (
    core,
    aws_lambda,
    aws_iam,
    aws_dynamodb
)

class S3infoToDynamodbStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #dynamodb
        s3_info_table01 = aws_dynamodb.Table(
            self,
            "s2infotable",
            table_name="s3-info",
            partition_key=aws_dynamodb.Attribute(
                name="s3_id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )
    
        #import lambda code
        try:
            with open("serverless_stack/functions/get_s3_info.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')

        #lambda function
        s3_info_function01 = aws_lambda.Function(
            self,
            "s3infofunction",
            function_name="S3InfoFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{s3_info_table01.table_name}"
            }
        )

        #s3 readonly policy to lambda
        s3_info_function01.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )
        )

        #dynamodb access to lambda
        s3_info_table01.grant_write_data(s3_info_function01)