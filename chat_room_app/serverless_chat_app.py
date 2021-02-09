from aws_cdk import (
    core,
    aws_ec2,
    aws_ecs,
    aws_ecs_patterns
)

class ServerlessChatAppStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #vpc
        chat_app_vpc = aws_ec2.Vpc(
            self,
            "ChatAppVpc",
            max_azs=2,
            nat_gateways=1
        )

        #fargate cluster
        chat_app_cluster = aws_ecs.Cluster(
            self,
            "ChatAppCluster"
        )

        #fargate task definition
        chat_app_fg_def = aws_ecs.FargateTaskDefinition(
            self,
            "ChatAppTaskDefinition"
        )

        #container definition
        chat_app_container = chat_app_fg_def.add_container(
            "ChatAppContainer",
            image=aws_ecs.ContainerImage.from_registry(
                "manuja/chat-app:latest"
            ),
            environment={
                "github": "https://github.com/manujakau"
            }
        )

        #port mapping to container
        chat_app_container.add_port_mappings(
            aws_ecs.PortMapping( container_port=3000, protocol=aws_ecs.Protocol.TCP)
        )

        #attached load balancer
        chat_app_alb = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "ChatAppALB",
            cluster=chat_app_cluster,
            task_definition=chat_app_fg_def,
            assign_public_ip=False,
            public_load_balancer=True,
            listener_port=80,
            desired_count=1,
            service_name="ServerlessChatApp"
        )

        #output
        chat_app_output = core.CfnOutput(
            self,
            "chatappoutput",
            value=f"http://{chat_app_alb.load_balancer.load_balancer_dns_name}",
            description="Chat app url"
        )