from aws_cdk import (
    core,
    aws_ec2,
    aws_ecs,
    aws_ecs_patterns
)

from aws_cdk.aws_applicationautoscaling import Schedule

class ServerlessBatchProcessStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #vpc
        batch_process_vpc = aws_ec2.Vpc(
            self,
            "BatchProcessVpc",
            max_azs=2,
            nat_gateways=1
        )

        #fargate cluster
        fargate_batch_process_cluster = aws_ecs.Cluster(
            self,
            "BatchProcessCluster",
            vpc=batch_process_vpc
        )

        #fargate with cloudwatch events rules
        batch_process_events = aws_ecs_patterns.ScheduledFargateTask(
            self,
            "BatchProcessEvent",
            cluster=fargate_batch_process_cluster,
            scheduled_fargate_task_image_options={
                "image": aws_ecs.ContainerImage.from_registry(
                    "manuja/demo-batch-process:latest"
                ),
                "memory_limit_mib":512,
                "cpu":256,
                "environment": {
                    "name": "TRIGGER",
                    "value": "cloudwatch events"
                }
            },
            schedule=Schedule.expression("rate(2 minutes)")
        )