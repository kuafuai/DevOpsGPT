$(document).ready(function () {
    getAppList()

    $("#add-application").click(function () {
        $('#app-edit').modal('show');
    });

    $("#app-edit-save").click(function () {
        var requestData = { 
            'app_name': $("#app_name").val(),
            'app_description': $("#app_description").val(),
            'app_default_source_branch': $("#app_default_source_branch").val(),
            'app_default_target_branch': $("#app_default_target_branch").val(),
            'service': []
        }
        serviceLen = $(".subservice").length+1
        for (var i = 1; i < serviceLen; i++) {
            var service = {
                'service_git_path' : $("#service_git_path_"+i).val(),
                'service_name' : $("#service_name_"+i).val(),
                'service_role' : $("#service_role_"+i).val(),
                'service_language' : $("#service_language_"+i).val(),
                'service_framework' : $("#service_framework_"+i).val(),
                'service_libs_name' : $("#service_libs_name_"+i).val(),
                'service_api_type' : $("#service_api_type_"+i).val(),
                'service_api_location' : $("#service_api_location_"+i).val(),
                'service_database' : $("#service_database_"+i).val(),
                'service_struct_cache' : $("#service_struct_cache_"+i).val(),
                'service_workflow' : $("#service_workflow_"+i).val(),
                'service_container_group' : $("#service_container_group_"+i).val(),
                'service_container_name' : $("#service_container_name_"+i).val(),
                'service_region' : $("#service_region_"+i).val(),
                'service_public_ip' : $("#service_public_ip_"+i).val(),
                'service_security_group' : $("#service_security_group_"+i).val(),
                'service_cd_subnet' : $("#service_cd_subnet_"+i).val()
            }
            requestData.service.push(service)
        }
        requestData = JSON.stringify(requestData)

        successCallback = function(data) {
            location.reload();
        }

        sendAjaxRequest('/app/create', 'POST', requestData, successCallback, alertErrorCallback, true, false)
    });

    $("#app-edit-cancel").click(function () {
        $('#app-edit').modal('hide');
    });

    $("#add-service").click(function(){
        subservice = $(".subservice")
        subserviceLen = subservice.length
        serviceID = subserviceLen+1
        str = `<div class="ui segment subservice" style="display: none;" id="subservice_`+serviceID+`">
                <h2 class="ui floated header">应用下子服务 `+serviceID+`</h2>
                <div class="field">
                <label>代码库路径</label>
                <div class="ui action input">
                    <input type="text" id="service_git_path_`+serviceID+`">
                    <button class="ui button" onClick="analyzeService(`+serviceID+`)" value="1"><span id="ai_analyze_service_icon"><i class="orange reddit square icon"></i></span>AI 代码分析</button>
                </div>
                </div>
                <div class="field">
                <label>服务名称</label>
                <input type="text" id="service_name_`+serviceID+`">
                </div>
                <div class="field">
                <label>服务用途</label>
                <input type="text" id="service_role_`+serviceID+`">
                </div>
                <div class="field">
                <label>开发语言</label>
                <input type="text" id="service_language_`+serviceID+`">
                </div>
                <div class="field">
                <label>开发框架</label>
                <input type="text" id="service_framework_`+serviceID+`">
                </div>
                <div class="field">
                <label>依赖 lib 包，用 , 分格</label>
                <input type="text" id="service_libs_name_`+serviceID+`">
                </div>
                <div class="field">
                <label>API 类型</label>
                <input type="text" id="service_api_type_`+serviceID+`">
                </div>
                <div class="field">
                <label>API 路径</label>
                <input type="text" id="service_api_location_`+serviceID+`">
                </div>
                <div class="field">
                <label>数据库</label>
                <input type="text" id="service_database_`+serviceID+`">
                </div>
                <div class="field">
                <label>应用代码结构</label>
                <textarea id="service_struct_cache_`+serviceID+`" rows="4"></textarea>
                </div>
                <div class="field">
                <label>CI - GitHub workflow</label>
                <input type="text" id="service_workflow_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - 容器组名称</label>
                <input type="text" id="service_container_group_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - 容器名称</label>
                <input type="text" id="service_container_name_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - 部署地域</label>
                <input type="text" id="service_region_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - 公网 IP</label>
                <input type="text" id="service_public_ip_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - 安全组</label>
                <input type="text" id="service_security_group_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - 子网/交换机</label>
                <input type="text" id="service_cd_subnet_`+serviceID+`">
                </div>
            </div>
        </div>`
        $("#add-service").after(str)
        $("#subservice_"+serviceID).slideDown("500")
        setTimeout(function () {
            $('#app-edit').modal('refresh');
        }, 550);
    });
});

function showApp(appID) {
    $('#app-edit').modal('show');
    
    var requestData = { 'app_id': appID }

    successCallback = function(data) {
        data = data.data.apps[0]
        console.log(data)
        $("#app_id").val(data.app_id)
        $("#app_default_source_branch").val(data.default_source_branch)
        $("#app_default_target_branch").val(data.default_target_branch)
        $("#app_description").val(data.description)
        $("#app_name").val(data.name)
        subservice = $(".subservice")
        subserviceLen = subservice.length
        serviceID = subserviceLen+1
        
        data.service.forEach(function (service, element_index, element_array) {
            serviceID = service.service_id
            libsStr = ""
            service.libs.forEach(function (lib, element_index, element_array) {
                libsStr += lib.sys_lib_name+","
            });
            libsStr = libsStr.replace(/,$/, '');
            str = `<div class="ui segment subservice" style="display: none;" id="subservice_`+serviceID+`">
                    <h2 class="ui floated header">应用下子服务 `+serviceID+`</h2>
                    <div class="field">
                    <label>代码库路径</label>
                    <div class="ui action input">
                        <input type="text" id="service_git_path_`+serviceID+`" value="`+service.git_path+`">
                        <button class="ui button" onClick="analyzeService(`+serviceID+`)" value="1"><span id="ai_analyze_service_icon"><i class="orange reddit square icon"></i></span>AI 代码分析</button>
                    </div>
                    </div>
                    <div class="field">
                    <label>服务名称</label>
                    <input type="text" id="service_name_`+serviceID+`" value="`+service.name+`">
                    </div>
                    <div class="field">
                    <label>服务用途</label>
                    <input type="text" id="service_role_`+serviceID+`" value="`+service.role+`">
                    </div>
                    <div class="field">
                    <label>开发语言</label>
                    <input type="text" id="service_language_`+serviceID+`" value="`+service.language+`">
                    </div>
                    <div class="field">
                    <label>开发框架</label>
                    <input type="text" id="service_framework_`+serviceID+`" value="`+service.framework+`">
                    </div>
                    <div class="field">
                    <label>依赖 lib 包，用 , 分格</label>
                    <input type="text" id="service_libs_name_`+serviceID+`" value="`+libsStr+`">
                    </div>
                    <div class="field">
                    <label>API 类型</label>
                    <input type="text" id="service_api_type_`+serviceID+`" value="`+service.api_type+`">
                    </div>
                    <div class="field">
                    <label>API 路径</label>
                    <input type="text" id="service_api_location_`+serviceID+`" value="`+service.api_location+`">
                    </div>
                    <div class="field">
                    <label>数据库</label>
                    <input type="text" id="service_database_`+serviceID+`" value="`+service.database+`">
                    </div>
                    <div class="field">
                    <label>应用代码结构</label>
                    <textarea id="service_struct_cache_`+serviceID+`" rows="4">`+service.struct_cache+`</textarea>
                    </div>
                    <div class="field">
                    <label>CI - GitHub workflow</label>
                    <input type="text" id="service_workflow_`+serviceID+`" value="`+service.git_workflow+`">
                    </div>
                    <div class="field">
                    <label>CD - 容器组名称</label>
                    <input type="text" id="service_container_group_`+serviceID+`" value="`+service.cd_container_group+`">
                    </div>
                    <div class="field">
                    <label>CD - 容器名称</label>
                    <input type="text" id="service_container_name_`+serviceID+`" value="`+service.cd_container_name+`">
                    </div>
                    <div class="field">
                    <label>CD - 部署地域</label>
                    <input type="text" id="service_region_`+serviceID+`" value="`+service.cd_region+`">
                    </div>
                    <div class="field">
                    <label>CD - 公网 IP</label>
                    <input type="text" id="service_public_ip_`+serviceID+`" value="`+service.cd_public_ip+`">
                    </div>
                    <div class="field">
                    <label>CD - 安全组</label>
                    <input type="text" id="service_security_group_`+serviceID+`" value="`+service.cd_security_group+`">
                    </div>
                    <div class="field">
                    <label>CD - 子网/交换机</label>
                    <input type="text" id="service_cd_subnet_`+serviceID+`" value="`+service.cd_subnet+`">
                    </div>
                </div>
            </div>`
            $("#add-service").after(str)
            $("#subservice_"+serviceID).slideDown("500")
            setTimeout(function () {
                $('#app-edit').modal('refresh');
            }, 550);
        });
    }

    sendAjaxRequest('/app/get', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function analyzeService(elementID) {
    $("#ai_analyze_service_icon").html('<i class="loading spinner icon"></i>')

    var requestData = JSON.stringify({ 'service_git_path': $("#service_git_path_"+elementID).val() })

    successCallback = function(data) {
        data = data.data
        $("#ai_analyze_service_icon").html('<i class="orange reddit square icon"></i>')
        console.log(data)
        console.log(elementID)
        $("#service_name_"+elementID).val(data.name)
        $("#service_role_"+elementID).val(data.role)
        $("#service_language_"+elementID).val(data.language)
        $("#service_framework_"+elementID).val(data.framework)
        $("#service_libs_name_"+elementID).val(data.service_libs_name)
        $("#service_api_type_"+elementID).val(data.service_api_type)
        $("#service_api_location_"+elementID).val(data.service_api_location)
        $("#service_database_"+elementID).val(data.database)
        $("#service_struct_cache_"+elementID).val(data.struct_cache)
        $("#service_git_workflow_"+elementID).val(data.git_workflow)
        $("#service_container_group_"+elementID).val(data.cd_container_group)
        $("#service_container_name_"+elementID).val(data.cd_container_name)
        $("#service_region_"+elementID).val(data.cd_region)
        $("#service_public_ip_"+elementID).val(data.cd_public_ip)
        $("#service_security_group_"+elementID).val(data.cd_security_group)
        $("#service_cd_subnet_"+elementID).val(data.cd_subnet)
    }

    sendAjaxRequest('/app/analyze_service', 'POST', requestData, successCallback, alertErrorCallback, true, false)
}

function getAppList() {
    requestData = ''

    successCallback = function(data) {
        apps = data.data.apps
        console.log(apps)

        var str = ""

        apps.forEach(function (app, element_index, element_array) {
            services = app["service"];
            servicesLen = services.length
            str += ` <tr style="cursor: pointer;" onClick="showApp(`+app["app_id"]+`)">
                        <td rowspan="`+servicesLen+`">`+app["name"]+`</td>
                        <td rowspan="`+servicesLen+`">`+app["description"]+`</td>
                        <td rowspan="`+servicesLen+`">`+app["default_source_branch"]+`</td>
                        <td rowspan="`+servicesLen+`">`+app["default_target_branch"]+`</td>
                        `
            services.forEach(function (service, element_index, element_array) {
                if (element_index==0) {
                    str += `
                            <td>`+service["name"]+`</td>
                            <td>`+service["role"]+`</td>
                            <td>`+service["language"]+`</td>
                            <td>`+service["framework"]+`</td>
                        </tr>`
                } else {
                    str += `<tr style="cursor: pointer;" onClick="showApp(`+app["app_id"]+`)">
                                <td>`+service["name"]+`</td>
                                <td>`+service["role"]+`</td>
                                <td>`+service["language"]+`</td>
                                <td>`+service["framework"]+`</td>
                            </tr>`
                }
            });
            $("#app_list").html(str)
        });
    }

    sendAjaxRequest('/app/get', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}