from flask import json
from app.pkgs.devops.cd_interface import CDInterface
from aliyunsdkcore.client import AcsClient
from aliyunsdkeci.request.v20180808.DescribeContainerGroupsRequest import DescribeContainerGroupsRequest
from aliyunsdkeci.request.v20180808 import CreateContainerGroupRequest
import time

class CDAliyun(CDInterface):
    def triggerCD(self, image, serviceInfo, cdConfig):
        self.client = AcsClient(cdConfig["ACCESS_KEY"], cdConfig["SECRET_KEY"], serviceInfo["cd_region"])
        # 创建ECI容器组
        request = CreateContainerGroupRequest.CreateContainerGroupRequest()
        request.set_ContainerGroupName(serviceInfo["cd_container_group"])
        request.set_RestartPolicy('Never')
        request.set_EipInstanceId(serviceInfo["cd_public_ip"])
        request.set_SecurityGroupId(serviceInfo["cd_security_group"])
        request.set_VSwitchId(serviceInfo["cd_subnet"])
        
        container_definition = {
            "Name": serviceInfo["cd_container_name"],
            "Image": image,
            "Cpu": 0.5,
            "Memory": 1,
            'ImagePullPolicy': "Always"
        }
        
        request.set_Containers([container_definition])
        
        response = self.client.do_action_with_exception(request)
        response_json = json.loads(response)
        container_group_id = response_json["ContainerGroupId"]
        print(container_group_id)
        print(response)

        # 等待容器组创建完成
        while True:
            try:
                time.sleep(10)
                request = DescribeContainerGroupsRequest()
                request.set_ContainerGroupIds([container_group_id])
                eci_info = self.client.do_action_with_exception(request)
                print(eci_info)
                eci_info_json = json.loads(eci_info)
                status = eci_info_json['ContainerGroups'][0]['Status']
                if status == 'Running':
                    break
            except Exception as e:
                print(str(e))
                break
        
        # 获取容器组的公网IP地址
        request = DescribeContainerGroupsRequest()
        request.set_ContainerGroupIds([container_group_id])
        eci_info = self.client.do_action_with_exception(request)
        eci_info_json = json.loads(eci_info)
        print(eci_info)
        public_ip = eci_info_json['ContainerGroups'][0]['InternetIp']
        
        return f'http://{public_ip}', True
