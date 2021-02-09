from aws_cdk import (
    aws_logs, core,
    aws_ec2,
    aws_rds
)

class WebAppRdsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, asg_secg, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #RDS db
        rds_db = aws_rds.DatabaseInstance(
            self,
            "rdsDB",
            database_name="testdb",
            engine=aws_rds.DatabaseInstanceEngine.MYSQL,
            vpc=vpc,
            port=3306,
            allocated_storage=20,
            multi_az=False,
            cloudwatch_logs_exports=[
                "error","general","slowquery"
            ],
            instance_type=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2,
                aws_ec2.InstanceSize.MICRO
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            delete_automated_backups=True,
            backup_retention=core.Duration.days(2)
        )
    
        for scg in asg_secg:
            rds_db.connections.allow_default_port_from(
                scg, "EC2 access to RDS"
            )
        
        #rds output
        outpur_rdsdb = core.CfnOutput(
            self,
            "rdsDBoutput",
            value=f"mysql -h {rds_db.db_instance_endpoint_address} -P 3306 -u admin -p",
            description="Connect to rds via EC2"
        )