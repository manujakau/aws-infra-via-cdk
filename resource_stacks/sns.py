from aws_cdk import (
    core,
    aws_sns 
)

import aws_cdk.aws_sns_subscriptions as aws_sns_subc

class SNSstack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #sns
        sns_topic = aws_sns.Topic(
            self,
            "snstopic01",
            display_name="Test Topic One",
            topic_name="TestTopic"
        )

        #add subscription to sns
        sns_topic.add_subscription(
            aws_sns_subc.EmailSubscription("mail@test.me")
        )
