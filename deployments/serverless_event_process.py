from aws_cdk import (
    core,
    aws_s3,
    aws_dynamodb,
    aws_lambda,
    aws_logs,
    aws_s3_notifications
)

class ServerlessEventProcessorStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #s3
        event_bucket = aws_s3.Bucket(
            self,
            "EventBucket",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #dynamodb
        event_table = aws_dynamodb.Table(
            self,
            "EventTable",
            table_name="event_table",
            partition_key=aws_dynamodb.Attribute(
                name="event_id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #import function code
        try:
            with open("deployments/functions/s3_events.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')

        #lambda function
        event_function = aws_lambda.Function(
            self,
            "EventFunction",
            function_name="Event_Processor",
            description="Process s3 Events",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{event_table.table_name}"
            }
        )

        #ddb write permissions
        event_table.grant_read_write_data(event_function)

        #logs
        event_logs = aws_logs.LogGroup(
            self,
            "EventLogs",
            log_group_name=f"/aws/lambda/{event_function.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.ONE_DAY
        )

        #s3 notifications
        event_notification = aws_s3_notifications.LambdaDestination(
            event_function
        )

        #event types to notify
        event_bucket.add_event_notification(
            aws_s3.EventType.OBJECT_CREATED,
            event_notification
        )