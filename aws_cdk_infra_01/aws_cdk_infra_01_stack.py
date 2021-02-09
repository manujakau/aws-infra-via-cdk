from aws_cdk import (
    core,
    aws_s3,
    aws_iam,
    aws_kms
)


class AwsCdkInfra01Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        aws_s3.Bucket(
            self, 
            "awscdk-infra",
            bucket_name="awscdk-infra-manuja",
            versioned=False,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL
        )

        mybucket = aws_s3.Bucket(
            self,
            "awscdk-infra-2"
        )

        aws_iam.Group(
            self,
            "gid"
        )

        output_1 = core.CfnOutput(
            self,
            "MyBucketOutput1",
            value=mybucket.bucket_name,
            description=f"Test CDK Bucket",
            export_name="MyBucketOutput1"
        )

#deploy to multienvironment
class ArtifactS3Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, is_prod=False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #parameter examples
        #print(self.node.try_get_context('prod')['kms_arn'])

        kms_key = aws_kms.Key.from_key_arn(
            self,
            "kmskeyid",
            self.node.try_get_context('envs')['prod']['kms_arn']
        )

        if is_prod:
            artifacts3 = aws_s3.Bucket(
                self,
                "ProdArtifacts3",
                versioned=True,
                encryption=aws_s3.BucketEncryption.KMS,
                encryption_key=kms_key,
                removal_policy=core.RemovalPolicy.DESTROY
            )

        else:
            artifacts3 = aws_s3.Bucket(
                self,
                "DevArtifacts3",
                removal_policy=core.RemovalPolicy.DESTROY
            )