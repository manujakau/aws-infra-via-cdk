from aws_cdk import (
    core,
    aws_lambda,
    aws_sns_subscriptions as aws_sns_subc,
    aws_cloudwatch as aws_cw,
    aws_cloudwatch_actions as aws_cw_ats,
    aws_logs
)


class CustomMetricsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #import function code
        try:
            with open("serverless_stack/functions/metric_logs_generator.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')
        
        #function
        function_01 = aws_lambda.Function(
            self,
            "lambdafunction01",
            function_name="LambdaTestCustomMEtric",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                'LOG_LEVEL': 'INFO',
                'PERCENTAGE_ERRORS': '75'
            }
        )

        #attached cloudwatch log group
        custom_metric_log_group01 = aws_logs.LogGroup(
            self,
            "cloudwatchlog01",
            log_group_name=f"/aws/lambda/{function_01.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.ONE_DAY
        )

        #Custom metric namespace
        custom_metric_namespace01 = aws_cw.Metric(
            namespace=f"custom-error-metric",
            metric_name="custom-error-metric",
            label="Amount of Custom API errors",
            period=core.Duration.minutes(1),
            statistic="Sum"
        )

        #Custom metric logs filter
        custom_metric_filter01 = aws_logs.MetricFilter(
            self,
            "customMetricFilter",
            filter_pattern=aws_logs.FilterPattern.boolean_value(
                "$.custom_api_error",
                True
            ),
            log_group=custom_metric_log_group01,
            metric_namespace=custom_metric_namespace01.namespace,
            metric_name=custom_metric_namespace01.metric_name,
            default_value=0,
            metric_value="1"
        )

        #create custom alarm
        custom_metric_alarm01 = aws_cw.Alarm(
            self,
            "customMetricAlarm",
            alarm_description="Custom API errors",
            alarm_name="Custom-API-alarm",
            metric=custom_metric_namespace01,
            comparison_operator=aws_cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            threshold=2,
            evaluation_periods=2,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(1),
            treat_missing_data=aws_cw.TreatMissingData.NOT_BREACHING
        )