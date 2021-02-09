from aws_cdk import (
    core,
    aws_s3
)

from aws_cdk import aws_s3_deployment

class DeployStaticWebPageStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #s3 bucket
        static_bucket = aws_s3.Bucket(
            self,
            "StaticBucket",
            versioned=True,
            public_read_access=True,
            website_index_document="index.html",
            website_error_document="404.html",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #import html files
        add_assets = aws_s3_deployment.BucketDeployment(
            self,
            "AssetsDeploy",
            sources=[
                aws_s3_deployment.Source.asset(
                    "deployments/assets"
                )
            ],
            destination_bucket=static_bucket
        )