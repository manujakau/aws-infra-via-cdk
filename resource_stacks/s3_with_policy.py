from aws_cdk import(
    core,
    aws_s3,
    aws_iam
)

class S3PolicyStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #s3 bucket
        cdk_bucket_01 = aws_s3.Bucket(
            self,
            "cdkBucket01",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #s3 resource policy
        cdk_bucket_01.add_to_resource_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[cdk_bucket_01.arn_for_objects("*.txt")],
                principals=[aws_iam.AnyPrincipal()]
            )
        )

        cdk_bucket_01.add_to_resource_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{cdk_bucket_01.bucket_arn}/*"],
                principals=[aws_iam.AnyPrincipal()],
                conditions={
                    "Bool": {"aws:SecureTransport": False}
                }
            )
        )
