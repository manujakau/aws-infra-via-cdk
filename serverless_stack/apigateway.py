from aws_cdk import (
    core,
    aws_lambda,
    aws_logs,
    aws_apigateway
)

class ApiGatewayStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #import function code
        try:
            with open("serverless_stack/functions/function-helloworld.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')

        #lambda
        function_01 = aws_lambda.Function(
            self,
            "lambdafunction01",
            function_name="LambdaTestAPIGW",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                'LOG_LEVEL': 'INFO',
                'Enviroment': 'Production'
            }
        )

        #attached cloudwatch log group
        log_group01 = aws_logs.LogGroup(
            self,
            "cloudwatchlog01",
            log_group_name=f"/aws/lambda/{function_01.function_name}",
            retention=aws_logs.RetentionDays.ONE_DAY,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #add API-GW
        api_gateway_function = aws_apigateway.LambdaRestApi(
            self,
            "apigateway01",
            handler=function_01
        )

        #output
        apigw_output = core.CfnOutput(
            self,
            "apigwOutput",
            value=f"{api_gateway_function.url}",
            description="web url for apigw"
        )