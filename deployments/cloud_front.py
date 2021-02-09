from aws_cdk import (
    core,
    aws_s3,
    aws_s3_deployment,
    aws_cloudfront
)

class DeployCloudFrontStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #s3 bucket
        static_bucket = aws_s3.Bucket(
            self,
            "StaticBucket",
            versioned=True,
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

        #add cloudfront origin access identity
        cloudfront_assets = aws_cloudfront.OriginAccessIdentity(
            self,
            "CloudfrontAssets",
            comment=f"CloudFront Assets for:{core.Aws.STACK_NAME}"
        )

        #cloudfront configuration
        cloudfront_config = aws_cloudfront.SourceConfiguration(
            s3_origin_source=aws_cloudfront.S3OriginConfig(
                s3_bucket_source=static_bucket,
                origin_access_identity=cloudfront_assets
            ),
            behaviors=[
                aws_cloudfront.Behavior(
                    is_default_behavior=True,
                    compress=True,
                    allowed_methods=aws_cloudfront.CloudFrontAllowedMethods.ALL,
                    cached_methods=aws_cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD
                )
            ]
        )

        #cloudfront distribution
        cloudfront_distribution = aws_cloudfront.CloudFrontWebDistribution(
            self,
            "CloudfrontDistribution",
            comment="CDN for static web",
            origin_configs=[
                cloudfront_config
            ],
            price_class=aws_cloudfront.PriceClass.PRICE_CLASS_100
        )

        #cloudfront url
        cloudfront_output = core.CfnOutput(
            self,
            "cloudfrontURL",
            value=f"{cloudfront_distribution.domain_name}",
            description="Static web page url"
        )