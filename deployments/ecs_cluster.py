from aws_cdk import (
    core,
    aws_ec2,
    aws_ecs,
    aws_ecs_patterns
)


class ECSclusterStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #vpc
        ecs_vpc = aws_ec2.Vpc(
            self,
            "EcsVpc",
            max_azs=2,
            nat_gateways=1
        )

        #ecs cluster
        ecs_cluster = aws_ecs.Cluster(
            self,
            "EcsCluster",
            vpc=ecs_vpc
        )

        #ecs cluster capacity
        ecs_cluster.add_capacity(
            "ecsClusterASGgroup",
            instance_type=aws_ec2.InstanceType("t2.micro")
        )

        #ecs attached to load balancer
        ecs_elb_service = aws_ecs_patterns.ApplicationLoadBalancedEc2Service(
            self,
            "EcsElb",
            cluster=ecs_cluster,
            memory_reservation_mib=512,
            task_image_options={
                "image": aws_ecs.ContainerImage.from_registry("httpd"),
                "environment": {
                    "ENVIRONMENT": "PROD"
                }
            }
        )

        #ecs elb url output
        ecs_output = core.CfnOutput(
            self,
            "ecsOutput",
            value=f"{ecs_elb_service.load_balancer.load_balancer_dns_name}",
            description="elb url"
        )