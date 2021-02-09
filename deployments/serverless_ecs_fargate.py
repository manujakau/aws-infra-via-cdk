from aws_cdk import (
    core,
    aws_ec2,
    aws_ecs,
    aws_ecs_patterns
)


class ServerlessEcsFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #vpc
        ecs_fargate_vpc = aws_ec2.Vpc(
            self,
            "EcsFargateVpc",
            max_azs=2,
            nat_gateways=1
        )

        #fargate
        fargate_cluster = aws_ecs.Cluster(
            self,
            "FargateCluster",
            vpc=ecs_fargate_vpc
        )

        #ecs-fargate attached to load balancer
        fargate_cluster_elb = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FargateWebService",
            cluster=fargate_cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options={
                "image": aws_ecs.ContainerImage.from_registry("httpd"),
                "environment": {
                    "ENVIRONMENT": "PROD"
                }                
            },
            desired_count=2
        )

        #health checks
        fargate_cluster_elb.target_group.configure_health_check(
            path="/"
        )

        #web url output
        fargate_output = core.CfnOutput(
            self,
            "FargateOutput",
            value=f"{fargate_cluster_elb.load_balancer.load_balancer_dns_name}"
        )