from aws_cdk import (
    core,
    aws_lambda,
    aws_logs,
    aws_events
)

from aws_cdk import aws_events_targets

class LAMBDAcronStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #import function code
        try:
            with open("serverless_stack/functions/function.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')

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
                'LOG_LEVEL': 'INFO'
            }
        )

        #attached cloudwatch log group
        log_group01 = aws_logs.LogGroup(
            self,
            "cloudwatchlog01",
            log_group_name=f"/aws/lambda/{function_01.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #cloudwatch event trigger on 6am
        cron_01 = aws_events.Rule(
            self,
            "cron01",
            schedule=aws_events.Schedule.cron(
                minute="0",
                hour="6",
                month="*",
                week_day="MON-FRI",
                year="*"
            )
        )

        #cloudwatch event trigger every 5min
        cron_02 = aws_events.Rule(
            self,
            "cron02",
            schedule=aws_events.Schedule.rate(
                core.Duration.minutes(5)
            )
        )

        #add triggers to lambda
        cron_01.add_target(
            aws_events_targets.LambdaFunction(
                function_01
            )
        )
        cron_02.add_target(
            aws_events_targets.LambdaFunction(
                function_01
            )
        )