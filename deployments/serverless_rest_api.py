from aws_cdk import (
    core,
    aws_dynamodb,
    aws_lambda,
    aws_apigateway,
    aws_logs
)

class ServerlessRestApiStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #dynamodb
        restapi_db = aws_dynamodb.Table(
            self,
            "ResetapiDB",
            partition_key=aws_dynamodb.Attribute(
                name="api_id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #import function code
        try:
            with open("deployments/functions/rest_api.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')
        
        #lambda
        api_function = aws_lambda.Function(
            self,
            "ApiFunction",
            function_name="rest_api_function",
            description="Invoke rest api",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{restapi_db.table_name}"
            }
        )

        #ddb write permissions
        restapi_db.grant_read_write_data(api_function)

        #logs
        event_logs = aws_logs.LogGroup(
            self,
            "EventLogs",
            log_group_name=f"/aws/lambda/{api_function.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.ONE_DAY
        )

        #build API
        api_01 = aws_apigateway.LambdaRestApi(
            self,
            "apifrontend",
            rest_api_name="api-frontend",
            handler=api_function,
            proxy=False
        )

        user_name = api_01.root.add_resource("{user_name}")
        add_user_likes = user_name.add_resource("{likes}")
        add_user_likes.add_method("GET")

        #api output
        api_output = core.CfnOutput(
            self,
            "apiurl",
            value=f"{add_user_likes.url}",
            description="replace user names"
        )