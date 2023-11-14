import boto3
from botocore.exceptions import ClientError
import datetime

# todo 未测试
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html
class CDAWS:    
    def triggerCD(self, image, serviceInfo, cdConfig):
        aws_service_name, aws_alb_name, aws_tg_name = self.generate_names_with_timestamp(serviceInfo["service_id"])

        # 创建 ALB 和 Target Group
        alb_arn, tg_arn, alb_dns_name, success = self.create_alb_and_target_group(cdConfig, serviceInfo, aws_alb_name, aws_tg_name)
        if not success:
            return f"Failed to create alb and target_grpup {alb_arn}", False

        # 创建 ECS 客户端
        client = boto3.client(
            'ecs',
            aws_access_key_id=cdConfig["ACCESS_KEY"],
            aws_secret_access_key=cdConfig["SECRET_KEY"],
            region_name=serviceInfo["cd_region"]
        )

        # 从 AWS Secrets Manager 获取配置好的 Secret 值，用于拉取私有库的镜像
        secret_name = "Docker"
        secret_value = self.get_secret(secret_name, cdConfig, serviceInfo)

        # 创建任务定义
        container_definition = {
            "name": serviceInfo["cd_container_name"],
            "image": image,
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
                family="testfamily",
                networkMode='awsvpc',
                requiresCompatibilities=['FARGATE'],
                cpu='2048',
                memory='4096',
                # https://cn-north-1.console.amazonaws.cn/iam/home#/roles/details/ecsTaskExecutionRole?section=permissions
                executionRoleArn=serviceInfo["cd_execution_role_arn"],
                containerDefinitions=[container_definition],
            )
        except Exception as e:
            return f"Error registering task definition: {str(e)}", False

        task_definition = response['taskDefinition']['taskDefinitionArn']

        print(f"Generated service_name: {aws_service_name}")
        try:
            # 创建或更新服务
            cd_cluster = 'KuaFuAIUser'
            existing_services = client.list_services(cluster=cd_cluster)
            if aws_service_name in existing_services["serviceArns"]:
                client.update_service(
                    cluster=cd_cluster,
                    service=aws_service_name,
                    desiredCount=1,  # 预定 1 个任务
                    taskDefinition=task_definition,
                )
            else:
                client.create_service(
                    cluster=cd_cluster,
                    serviceName=aws_service_name,
                    taskDefinition=task_definition,
                    desiredCount=1,  # 预定 1 个任务
                    launchType='FARGATE',
                    networkConfiguration={
                        'awsvpcConfiguration': {
                            'subnets': [serviceInfo["cd_subnet"], "subnet-02a884ac1c7bd0519"],
                            'securityGroups': [serviceInfo["cd_security_group"]],
                            'assignPublicIp': 'ENABLED'
                        }
                    },
                    loadBalancers=[
                        {
                            'targetGroupArn': tg_arn,
                            'containerName': serviceInfo["cd_container_name"],
                            'containerPort': 80     # 容器的监听端口

                        }
                    ],
                )
        except Exception as e:
            return f"Error creating/updating service: {str(e)}", False

        return f'访问网址：http://{alb_dns_name}:8086 （本环境仅供体验，1小时后将自动删除。This environment is for experience only and will be deleted after 1 hour）', True
    
    def generate_names_with_timestamp(self, service_id):
        # 获取当前时间并格式化为小时和分钟
        timestamp = datetime.datetime.now().strftime('%H%M')

        # 生成资源名称，服务名称除外，它将从cdConfig中获取
        albname = f"User-alb-{service_id}-{timestamp}"
        tgname = f"User-tg-{service_id}-{timestamp}"
        service_name = f"User-Service-{service_id}-{timestamp}"

        return service_name, albname, tgname,

    def create_alb_and_target_group(self, cdConfig, serviceInfo, albname, tgname):
        elbv2_client = boto3.client(
            'elbv2',
            aws_access_key_id=cdConfig["ACCESS_KEY"],
            aws_secret_access_key=cdConfig["SECRET_KEY"],
            region_name=serviceInfo["cd_region"]
        )

        try:
            # 创建 ALB
            alb_response = elbv2_client.create_load_balancer(
                Name=albname,
                Subnets=[serviceInfo["cd_subnet"], serviceInfo["cd_subnet2"]],
                SecurityGroups=[serviceInfo["cd_security_group"]],
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
                VpcId= serviceInfo["cd_vpc"],  # https://console.amazonaws.cn/vpc/home?region=cn-north-1#vpcs:
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
    
    def get_secret(self, secret_name, cdConfig, serviceInfo):
        # 创建 ECS 客户端
        client = boto3.client(
            'secretsmanager',
            aws_access_key_id=cdConfig["ACCESS_KEY"],
            aws_secret_access_key=cdConfig["SECRET_KEY"],
            region_name=serviceInfo["cd_region"]
        )

        # 在 try 块中尝试检索 secret
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # 如果没有找到密钥或发生其他错误，打印错误消息
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager 不能解密受保护的 secret 文本
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # 发生内部服务错误
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # 提供的参数无效
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # 提供的请求无效
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # 未找到指定的 secret
                raise e
            else:
                # 未知错误
                raise e
        else:
            # 如果 secret 使用了字符串，则直接返回它
            if 'SecretString' in get_secret_value_response:
                return get_secret_value_response['SecretString']
            # 否则，返回二进制值
            else:
                return get_secret_value_response['SecretBinary']