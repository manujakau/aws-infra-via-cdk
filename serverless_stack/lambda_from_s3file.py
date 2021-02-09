from aws_cdk import (
    core,
    aws_lambda,
    aws_logs,
    aws_s3
)

class LAMBDAfromS3Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #import s3
        test_s3 = aws_s3.Bucket.from_bucket_attributes(
            self,
            "tests3",
            bucket_name="manuja-test1"
        )

        #lambda
        test_func01 = aws_lambda.Function(
            self,
            "testlambda",
            function_name="lambdaFromS3",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="function.lambda_handler",
            code=aws_lambda.S3Code(
                bucket=test_s3,
                key="lambda/function.zip"
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1
        )

        #attached cloudwatch log group
        log_group01 = aws_logs.LogGroup(
            self,
            "cloudwatchlog01",
            log_group_name=f"/aws/lambda/{test_func01.function_name}",
            retention=aws_logs.RetentionDays.ONE_DAY,
            removal_policy=core.RemovalPolicy.DESTROY
        )