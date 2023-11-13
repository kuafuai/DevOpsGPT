import boto3
from botocore.exceptions import ClientError
import datetime

# todo 未测试
class CDAWS:
    def generate_names_with_timestamp(self, cdConfig):
        # 获取当前时间并格式化为小时和分钟
        timestamp = datetime.datetime.now().strftime('%H%M')

        # 生成资源名称，服务名称除外，它将从cdConfig中获取
        albname = f"User-alb-{timestamp}"
        tgname = f"User-tg-{timestamp}"
        service_name = f"User-Service-{timestamp}"

        return service_name, albname, tgname,

    def create_alb_and_target_group(self, cdConfig):
        service_name, albname, tgname = self.generate_names_with_timestamp(cdConfig)
        elbv2_client = boto3.client(
            'elbv2',
            aws_access_key_id=cdConfig["ACCESS_KEY"],
            aws_secret_access_key=cdConfig["SECRET_KEY"],
            region_name=cdConfig["cd_region"]
        )

        try:
            # 创建 ALB
            alb_response = elbv2_client.create_load_balancer(
                Name=albname,
                Subnets=[cdConfig["cd_subnet1"], cdConfig["cd_subnet2"]],
                SecurityGroups=[cdConfig["cd_security_group"]],
                Scheme='internet-facing',
                Tags=[{
                    'Key': 'Name',
                    'Value': 'my-alb'
                }]
            )
            alb_arn = alb_response['LoadBalancers'][0]['LoadBalancerArn']
            alb_dns_name = alb_response['LoadBalancers'][0]['DNSName']

            # 创建 Target Group
            tg_response = elbv2_client.create_target_group(
                Name=tgname,
                Protocol='HTTP',
                Port=80,   # 注意：确保这个端口号与容器监听端口一致
                VpcId=cdConfig["cd_vpc_id"],
                TargetType='ip',
                HealthCheckProtocol='HTTP',  # 指定健康检查协议
                HealthCheckPort='80',  # 指定健康检查端口
                HealthCheckPath='/',  # 指定健康检查路径
                HealthCheckIntervalSeconds=30,  # 指定健康检查间隔
                HealthCheckTimeoutSeconds=5,  # 指定健康检查超时
                HealthyThresholdCount=2,  # 指定健康阈值
                UnhealthyThresholdCount=2,  # 指定不健康阈值
            )

            tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']

            # 创建 Listener
            listener_response = elbv2_client.create_listener(
                LoadBalancerArn=alb_arn,
                Protocol='HTTP',
                Port=8086,
                DefaultActions=[
                    {
                        'Type': 'forward',
                        'TargetGroupArn': tg_arn
                    }
                ]
            )

            return alb_arn, tg_arn, alb_dns_name, True
        except Exception as e:
            return f"Error creating ALB and Target Group: {str(e)}", None, None, False
    
    def triggerCD(self, image, serviceInfo, cdConfig):

        # 创建 ECS 客户端
        client = boto3.client(
            'ecs',
            aws_access_key_id=cdConfig["ACCESS_KEY"],
            aws_secret_access_key=cdConfig["SECRET_KEY"],
            region_name=cdConfig["cd_region"]
        )

        # 创建 ALB 和 Target Group
        alb_arn, tg_arn, alb_dns_name, success = self.create_alb_and_target_group(cdConfig)
        if not success:
            return alb_arn, False  # alb_arn 在这里实际上是一个错误消息

        # 从 AWS Secrets Manager 获取 Secret 值
        secret_name = "Docker"  # 您可以根据实际需求进行更改
        secret_value = self.get_secret(secret_name, cdConfig)

        # 创建任务定义
        container_definition = {
            "name": cdConfig["cd_container_name"],
            "image": 'registry.cn-hangzhou.aliyuncs.com/kuafuai/test',
            "cpu": 1024,  # 0.5 vCPU
            "memory": 2048,  # 2GB RAM
            "essential": True,
            "portMappings": [
                {'containerPort': 80,
                 'hostPort': 80,
                 'protocol': 'tcp'},
                ],
                 "environment": [  # 示例：将 secret_value 作为环境变量
            {
                "name": "SECRET_KEY",
                "value": secret_value
            }
        ]
        }

        try:
            response = client.register_task_definition(
                family=cdConfig["cd_task_family"],
                networkMode='awsvpc',
                requiresCompatibilities=['FARGATE'],
                cpu='2048',
                memory='4096',
                executionRoleArn=cdConfig["executionRoleArn"],
                containerDefinitions=[container_definition],
            )
        except Exception as e:
            return f"Error registering task definition: {str(e)}", False

        task_definition = response['taskDefinition']['taskDefinitionArn']

        # 使用 generate_names_with_timestamp 方法生成服务名称
        service_name, albname, tgname = self.generate_names_with_timestamp(cdConfig)
        print(f"Generated service_name: {service_name}")
        try:
            # 创建或更新服务
            existing_services = client.list_services(cluster=cdConfig["cd_cluster"])
            if service_name in existing_services["serviceArns"]:
                client.update_service(
                    cluster=cdConfig["cd_cluster"],
                    service=service_name,
                    desiredCount=1,  # 预定 1 个任务
                    taskDefinition=task_definition,
                )
            else:
                client.create_service(
                    cluster=cdConfig["cd_cluster"],
                    serviceName=service_name,
                    taskDefinition=task_definition,
                    desiredCount=1,  # 预定 1 个任务
                    launchType='FARGATE',
                    networkConfiguration={
                        'awsvpcConfiguration': {
                            'subnets': [cdConfig["cd_subnet1"], cdConfig["cd_subnet2"]],
                            'securityGroups': [cdConfig["cd_security_group"]],
                            'assignPublicIp': 'ENABLED'
                        }
                    },
                    loadBalancers=[
                        {
                            'targetGroupArn': tg_arn,
                            'containerName': cdConfig["cd_container_name"],
                            'containerPort': 80     # 容器的监听端口

                        }
                    ],
                )
        except Exception as e:
            return f"Error creating/updating service: {str(e)}", False
        except ClientError as e:
            # 如果 AWS 报告了客户端错误，返回错误信息
            return f"Error creating/updating service with AWS ClientError: {str(e)}", False
        except ValueError as e:
            # 如果 service_name 为空，返回错误信息
            return f"Error with 'service_name': {str(e)}", False
        except Exception as e:
            # 如果遇到了其他错误，返回错误信息
            return f"An unexpected error occurred: {str(e)}", False
        return f'访问网址：http://{alb_dns_name}:8086 （本环境仅供体验，1小时后将自动删除。This environment is for experience only and will be deleted after 1 hour）', True