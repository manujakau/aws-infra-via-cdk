from aws_cdk import core
from aws_cdk import aws_dynamodb

class DYNAMOdbStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #dynamodb
        dynamodb_table01 = aws_dynamodb.Table(
            self,
            "dynamodb01",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            server_side_encryption=True
        )