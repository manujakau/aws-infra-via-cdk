from aws_cdk import (
    core,
    aws_sqs 
)
from aws_cdk.aws_sns import Topic

class SQSstack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #SQS
        sqs_queue = aws_sqs.Queue(
            self,
            "sqsqueue",
            queue_name="testSQSqueue.fifo",
            fifo=True,
            encryption=aws_sqs.QueueEncryption.KMS_MANAGED,
            retention_period=core.Duration.days(2),
            visibility_timeout=core.Duration.seconds(45)
        )