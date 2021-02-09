from aws_cdk import core
import json


class CFNimportstack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #import from cloud-formation template
        try:
            with open("import_from_cfn/s3.json", mode="r") as file:
                cfn_template = json.load(file)
        except OSError:
            print("CFN Read error")

        import_from_cfn = core.CfnInclude(
            self,
            "importfromcfn",
            template=cfn_template
        )

        s3_bucket_arn = core.Fn.get_att("S3Bucket", "Arn")

        #output

        output_s3 = core.CfnOutput(
            self,
            "s3arnoutput",
            value=f"{s3_bucket_arn.to_string()}",
            description="arn for s3 from imported cfn"
        )