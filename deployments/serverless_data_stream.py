from aws_cdk import (
    core,
    aws_s3,
    aws_lambda,
    aws_logs,
    aws_s3_notifications,
    aws_kinesis,
    aws_iam
)

from aws_cdk import aws_lambda_event_sources as aws_lambda_es

class ServerlessDataStreamStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #kinesis data stream
        kinesis_stream = aws_kinesis.Stream(
            self,
            "kinesisStream",
            retention_period=core.Duration.hours(24),
            shard_count=1,
            stream_name="kinesis_test_data_pipe"
        )

        #s3 for store stream data events
        kinesis_s3_bucket = aws_s3.Bucket(
            self,
            "kinesisS3Bucket",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #Lambda functions

        #import function codes - data consume
        try:
            with open("deployments/functions/stream_data_get.py", mode="r") as file:
                function_body_get = file.read()
        except OSError:
            print('File can not read')
        
        #consume function
        stream_get_function = aws_lambda.Function(
            self,
            "consumeFunction",
            function_name="StreamConsumeFunction",
            description="Process Data Streams and store to s3",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body_get
            ),
            timeout=core.Duration.seconds(5),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "BUCKET_NAME": f"{kinesis_s3_bucket.bucket_name}"                
            }
        )

        #permision to use stream by lambda
        kinesis_stream.grant_read(
            stream_get_function
        )

        #s3 permision
        lambdas3Permision = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            resources=[
                f"{kinesis_s3_bucket.bucket_arn}/*"
            ],
            actions=[
                "s3:PutObject"
            ]
        )
        lambdas3Permision.sid="S3writePermisionToLambda"
        stream_get_function.add_to_role_policy(lambdas3Permision)

        #logs
        stream_concume_logs = aws_logs.LogGroup(
            self,
            "StreamConcumeLogs",
            log_group_name=f"/aws/lambda/{stream_get_function.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.ONE_DAY
        )

        #kinesis event source
        kinesis_event_sources = aws_lambda_es.KinesisEventSource(
            stream=kinesis_stream,
            starting_position=aws_lambda.StartingPosition.LATEST,
            batch_size=1
        )

        #attached kinesis to lambda
        stream_get_function.add_event_source(kinesis_event_sources)


        #generate stream lambda function#####

        #import function codes - data consume
        try:
            with open("deployments/functions/stream_data_gen.py", mode="r") as file:
                function_body_gen = file.read()
        except OSError:
            print('File can not read')

        #stream generate function
        stream_gen_function = aws_lambda.Function(
            self,
            "GenarateFunction",
            function_name="StreamGenerateFunction",
            description="Generate Data Streams",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.lambda_handler",
            code=aws_lambda.InlineCode(
                function_body_gen
            ),
            timeout=core.Duration.seconds(60),
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "STREAM_NAME": f"{kinesis_stream.stream_name}"  
            }
        )

        #permision to lambda to write into kinesis
        kinesis_stream.grant_read_write(stream_gen_function)

        #logs
        stream_generate_logs = aws_logs.LogGroup(
            self,
            "StreamGenerateLogs",
            log_group_name=f"/aws/lambda/{stream_gen_function.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=aws_logs.RetentionDays.ONE_DAY
        )