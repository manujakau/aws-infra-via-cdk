from aws_cdk import (
    core,
    aws_lambda,
    aws_lambda_event_sources as aws_lambda_es,
    aws_dynamodb
)


class ServerlessDynamoDBStreamStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #dynamodb
        stream_dynamodb = aws_dynamodb.Table(
            self,
            "StreamDynamoDb",
            partition_key=aws_dynamodb.Attribute(
                name="stream_id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            stream=aws_dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #import lambda code
        try:
            with open("deployments/functions/ddb_stream.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')

        #lambda
        ddb_stream_function = aws_lambda.Function(
            self,
            "DddbStreamFunction",
            function_name="DynamoDbStream",
            description="Dynamodb stream processor",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
            }
        )

        #dynamodb stream event sources
        dynamodb_event_source = aws_lambda_es.DynamoEventSource(
            table=stream_dynamodb,
            starting_position=aws_lambda.StartingPosition.TRIM_HORIZON,
            bisect_batch_on_error=True
        )

        #lambda trigger
        ddb_stream_function.add_event_source(dynamodb_event_source)