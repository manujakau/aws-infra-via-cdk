#!/usr/bin/env python3

from attr import __description__
from aws_cdk import core

#from aws_cdk_infra_01.aws_cdk_infra_01_stack import AwsCdkInfra01Stack, ArtifactS3Stack
#from resource_stacks.vpc import VPCStack
#from resource_stacks.ec2 import EC2Stack
#from resource_stacks.ec2_with_profile import EC2StackWithRoles

#web app with vpc asg and alb
#from full_stacks.web_app_vpc import WebAppVPCStack
#from full_stacks.web_app_infra import WebAppInfraStack

#SSM
#from resource_stacks.ssm import SSMStack

#IAM
#from resource_stacks.iam import IAMStack

#S3 with policy
#from resource_stacks.s3_with_policy import S3PolicyStack

#3tier web app
#from rds_full_stack.web_app_infra import WebAppInfraStack
#from rds_full_stack.web_app_vpc import WebAppVPCStack
#from rds_full_stack.web_app_rds import WebAppRdsStack

#import from cfn template
#from import_from_cfn.import_from_cfn import CFNimportstack

#SNS
#from resource_stacks.sns import SNSstack

#SQS
#from resource_stacks.sqs import SQSstack

#serverless stack
#from serverless_stack.serverless import LAMBDAStack

#serverless stack from s3 upload code
#from serverless_stack.lambda_from_s3file import LAMBDAfromS3Stack

#lambda with cloudwatch triggers
#from serverless_stack.lambda_cronjobs import LAMBDAcronStack

#dynamodb
#from serverless_stack.dynamodb import DYNAMOdbStack

#s3 info to dynamodb
#from serverless_stack.s3_info_to_ddb import S3infoToDynamodbStack

#apigw
#from serverless_stack.apigateway import ApiGatewayStack

#Monitor Stack
#from monitor_stack.ec2_webapp_alram import MonitoringStack

#Custom metric stack
#from monitor_stack.custom_metrics import CustomMetricsStack

#Custom Dashboard stack
#from monitor_stack.cloudwatch_dashboard import CustomDashBoardStack

#deploy static webpage
#from deployments.static_website import DeployStaticWebPageStack

#deploy static webpage with cloudfront
#from deployments.cloud_front import DeployCloudFrontStack

#deploy serverless event notifications
#from deployments.serverless_event_process import ServerlessEventProcessorStack

#deploy rest api
#from deployments.serverless_rest_api import ServerlessRestApiStack

#Serverless Data streaming
#from deployments.serverless_data_stream import ServerlessDataStreamStack

#dynamodb stremimg
#from deployments.dynamodb_stream import ServerlessDynamoDBStreamStack

#ecs cluster
#from deployments.ecs_cluster import ECSclusterStack

#fargate cluster
#from deployments.serverless_ecs_fargate import ServerlessEcsFargateStack

#batch process via fargate
#from deployments.fargate_batch_process import ServerlessBatchProcessStack

#chat app
from chat_room_app.serverless_chat_app import ServerlessChatAppStack

app = core.App()

#AwsCdkInfra01Stack(app, "aws-cdk-infra-01")

#parameters example
#print(app.node.try_get_context('prod')['region'])

#variables
#env_us = core.Environment(region="us-east-1")
#env_eu = core.Environment(region=app.node.try_get_context('envs')['prod']['region'])

#multiy env setup
#ArtifactS3Stack(app, "DevStack", env=env_us)
#ArtifactS3Stack(app, "ProdStack", is_prod=True, env=env_eu)

#Basic VPC
#VPCStack(app, "custom-vpc-stack")

#VPC with exsisting resources
#VPCStack(app, "custom-vpc-stack", env=core.Environment(
#                                            account=app.node.try_get_context('envs')['prod']['aws_account_id'],
#                                            region=app.node.try_get_context('envs')['prod']['region']))

#global tags
#core.Tag.add(app, 
#            key="support_email",
#            value=app.node.try_get_context('envs')['prod']['support_email'])

#EC2 deploy on default vpc
#EC2Stack(app, "test-server-01", env=core.Environment(
#                                            account=app.node.try_get_context('envs')['default']['aws_account_id'],
#                                            region=app.node.try_get_context('envs')['default']['region']))

#EC2 with instances profile deploy on default vpc
#EC2StackWithRoles(app, "test-server-01", env=core.Environment(
#                                            account=app.node.try_get_context('envs')['default']['aws_account_id'],
#                                            region=app.node.try_get_context('envs')['default']['region']))

#web app with vpc asg and alb
#vpc_stack = WebAppVPCStack(app, "webapp-vpc-stack")
#ec2_stack = WebAppInfraStack(app, "web-app-stack", vpc=vpc_stack.custom_vpc)

#SSMstack
#ssm_stack = SSMStack(app, "ssm-stack", description="SSM parameter stack", env=core.Environment(
#                                            account=app.node.try_get_context('envs')['default']['aws_account_id'],
#                                            region=app.node.try_get_context('envs')['default']['region']))

#IAM
#iam_stack = IAMStack(app, "iam-stack")

#S3 with policy
#s3Policy_stack = S3PolicyStack(app, "s3Policy-stack")

#3tier web app
#app_3tier_vpc = WebAppVPCStack(app, "webapp-vpc")
#app_3tier_infra = WebAppInfraStack(app, "webapp-infra", 
#                                        vpc=app_3tier_vpc.custom_vpc)
#app_3tier_rds = WebAppRdsStack(app, "webapp-rds", 
#                                    vpc=app_3tier_vpc.custom_vpc,
#                                    asg_secg=app_3tier_infra.web_app_lc_asg.connections.security_groups,
#                                    description="RDS Database")

#import from cfn template
#import_stack = CFNimportstack(app, "import-cfn-stack")

#SNS
#sns_stack = SNSstack(app, "sns-stack")

#SQS
#sqs_stack = SQSstack(app, "sqs-stack")

#serverless stack
#lambda_stack = LAMBDAStack(app, "lambda-stack")

#serverless stack from s3 upload code
#lambda_from_s3code = LAMBDAfromS3Stack(app, "lambda-import-s3code")

#lambda with cloudwatch triggers
#lambda_cron_invoke = LAMBDAcronStack(app, "lambda-cron-stack")

#dynamodb
#dynamodb_stack = DYNAMOdbStack(app, "dynamodb-stack")

#s3 info to dynamodb
#s3_info_to_dynamodb_stack = S3infoToDynamodbStack(app, "s3-info-to-ddb-stack")

#apigw
#apigw_stack = ApiGatewayStack(app, "apigw-stack")

#Monitor Stack
#monitor_stack = MonitoringStack(app, "monitor-stack")

#custom metrics
#custom_metric_stack = CustomMetricsStack(app, "custom-metric-stack")

#custom dashboard stack
#custom_dashboard_stack = CustomDashBoardStack(app, "custom-dashboard-stack")

#deploy static webpage
#static_web_stack = DeployStaticWebPageStack(app, "static-web-stack")

#deploy static webpage with cloudfront
#cloudfront_stack = DeployCloudFrontStack(app, "cloudfront-stack")

#deploy serverless event notifications
#serverless_event_notify_stack = ServerlessEventProcessorStack(app, "serverless-events-notify-stack")

#deploy rest api
#rest_api_stack = ServerlessRestApiStack(app, "rest-api-stack")

#Serverless Data Streaming
#serverless_data_stream_stack = ServerlessDataStreamStack(app, "serverless-data-stream-stack")

#dynamodb streaming
#serverless_ddb_streaming = ServerlessDynamoDBStreamStack(app, "serverless-ddb-stream-stack")

#ecs cluster
#ecs_stack = ECSclusterStack(app, "ecs-cluster")

#fargate cluster
#fargate_stack = ServerlessEcsFargateStack(app, "fargate-stack")

#batch process via fargate
#batch_process_stack = ServerlessBatchProcessStack(app, "batch-process-stack")

#chat app
chat_app_stack = ServerlessChatAppStack(app, "chat-app-stack")

app.synth()