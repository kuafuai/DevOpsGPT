$(document).ready(function () {
    getAppList()

    action = getAction()
    if (action == "create_new" || action == "create_new_ai" || action == "create_new_tpl") {
        setTimeout(function () {
            $("#add-application").click()
        }, 1000);
    }

    // show dropdown on hover
    $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
    });

    $("#add-application").click(function () {
        cleanUpApp()
        rendSelect()
        getAppTplList()

        $("#app-new-way1").removeClass('hideitem');
        $("#app-new-way2").removeClass('hideitem');
        $("#app-new-way").removeClass('hideitem');
        if (action == "create_new_ai") {
            $("#app-new-way1").addClass('hideitem');
            $("#app-new-way").addClass('hideitem');
        }
        if (action == "create_new_tpl") {
            $("#app-new-way2").addClass('hideitem');
            $("#app-new-way").addClass('hideitem');
        }
        $('#app-new').modal('show');
    });

    $("#app-edit-save").click(function () {
        appCreateErrorCallback = function(error) {
            $("#app-message").html(error)
            $("#app-message").fadeOut().fadeIn()
    
            setTimeout(function () {
                $("#app-message").fadeOut();
            }, 6000);
        }

        var requestData = { 
            'app_id': $("#app_id").val(),
            'app_git_config': $("#app_git_config").val(),
            'app_ci_config': $("#app_ci_config").val(),
            'app_cd_config': $("#app_cd_config").val(),
            'app_name': $("#app_name").val(),
            'app_description': $("#app_description").val(),
            'app_default_source_branch': $("#app_default_source_branch").val(),
            'app_default_target_branch': $("#app_default_target_branch").val(),
            'service': []
        }

        var err_msg = ''
        if (requestData.app_name.length < 2) {
            err_msg = "The 'APP name' field cannot be empty. '应用名称'字段不能为空。"
        }
        if (requestData.app_description.length < 2) {
            err_msg = "The 'APP introduction' field cannot be empty. '应用介绍'字段不能为空。"
        }
        if (err_msg.length > 0) {
            appCreateErrorCallback(err_msg)
            return
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
                'service_security_group' : $("#service_security_group_"+i).val(),
                'service_cd_subnet' : $("#service_cd_subnet_"+i).val(),
                'service_service_type' : $("#service_service_type_"+i).val(),
                'service_cd_subnet2' : $("#service_cd_subnet2_"+i).val(),
                'service_cd_vpc' : $("#service_cd_vpc_"+i).val(),
                'service_cd_execution_role_arn' : $("#service_cd_execution_role_arn_"+i).val(),
            }
            requestData.service.push(service)
        }
        requestData = JSON.stringify(requestData)

        successCallback = function(data) {
            window.location.href = "/app.html"
        }

        sendAjaxRequest('/app/create', 'POST', requestData, successCallback, appCreateErrorCallback, true, false)
    });

    $("#app-edit-cancel").click(function () {
        window.location.href = "/app.html"
    });
    $(".f_cancel").click(function () {
        $('#app-new').modal('hide');
    });

    $("#app-app-save").click(function(){
        git_path = $("#ai_code_analysis_git_path").val()
        $('#app-edit').modal('setting', 'closable', false).modal('show');
        $("#add-service").click();
        $("#service_git_path_1").val(git_path);
        analyzeService(1)
    });

    $("#app-tpl-save").click(function(){
        tpl_id = $("#tpl_select").val()
        showApp(tpl_id, true)
    });

    $("#add-service").click(function(){
        subservice = $(".subservice")
        subserviceLen = subservice.length
        serviceID = subserviceLen+1
        str = `<div class="ui segment subservice" style="display: none;" id="subservice_`+serviceID+`">
                <h2 class="ui floated header">`+globalFrontendText["app_sub_service"]+` `+serviceID+`</h2>
                <div class="field">
                <label>`+globalFrontendText["git_path"]+`</label>
                <div class="ui action input">
                    <input type="text" id="service_git_path_`+serviceID+`">
                    <button class="purple ui button ai_analyze_service_btn" onClick="analyzeService(`+serviceID+`)" value="1"><span id="ai_analyze_service_icon"><i class=" reddit square icon"></i></span>`+globalFrontendText["ai_code_analysis"]+`</button>
                </div>
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_name"]+`</label>
                <input type="text" id="service_name_`+serviceID+`">
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_type"]+`</label>
                <select class="ui fluid dropdown" id="service_service_type_`+serviceID+`">
                    <option value="FRONTEND">前端/移动端（Frontend/Mobile）</option>
                    <option value="BACKEND">后端服务（Backend）</option>
                    <option value="FRONTEND_BACKEND">前端+后端（Frontend + Backend）</option>
                    <option value="GAME">游戏（GAME）</option>
                    <option value="COMMON">其它（Others）</option>
                </select>
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_role"]+`</label>
                <textarea id="service_role_`+serviceID+`" rows="4"></textarea>
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_language"]+`</label>
                <input type="text" id="service_language_`+serviceID+`">
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_framework"]+`</label>
                <input type="text" id="service_framework_`+serviceID+`">
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_libs"]+`</label>
                <input type="text" id="service_libs_name_`+serviceID+`">
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_api_type"]+`</label>
                <input type="text" id="service_api_type_`+serviceID+`">
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_api_path"]+`</label>
                <input type="text" id="service_api_location_`+serviceID+`">
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_database"]+`</label>
                <input type="text" id="service_database_`+serviceID+`">
                </div>
                <div class="field">
                <label>`+globalFrontendText["service_code_struct"]+`</label>
                <textarea id="service_struct_cache_`+serviceID+`" rows="4"></textarea>
                </div>
                <div class="field">
                <label>CI - GitHub workflow</label>
                <input type="text" id="service_workflow_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - GROUP</label>
                <input type="text" id="service_container_group_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - NAME</label>
                <input type="text" id="service_container_name_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - REGION</label>
                <input type="text" id="service_region_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - SECURITY GROUP</label>
                <input type="text" id="service_security_group_`+serviceID+`">
                </div>
                <div class="field">
                <label>CD - SUBNET/SWITCH</label>
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

function removeSubservice(idx){
    $("#subservice_"+idx).remove()
}

function showApp(appID, isTpl) {
    cleanUpApp()
    rendSelect()
    $('#app-edit').modal('setting', 'closable', false).modal('show');
    
    var requestData = { 'app_id': appID }

    successCallback = function(data) {
        data = data.data.apps[0]
        console.log(data)
        if (!isTpl) {
            $("#app_id").val(data.app_id)
        }
        $("#app_default_source_branch").val(data.default_source_branch)
        $("#app_default_target_branch").val(data.default_target_branch)
        if (!isTpl) {
            $("#app_description").val(data.description)
            $("#app_name").val(data.name)
        }
        $("#app_git_config").val(data.git_config),
        $("#app_ci_config").val(data.ci_config),
        $("#app_cd_config").val(data.cd_config),
        subservice = $(".subservice")
        subserviceLen = subservice.length
        serviceID = subserviceLen+1
        
        data.service.forEach(function (service, ele_idx, element_array) {
            idx = ele_idx+1
            serviceID = service.service_id
            libsStr = ""
            service.libs.forEach(function (lib, element_index, element_array) {
                libsStr += lib.sys_lib_name+","
            });
            libsStr = libsStr.replace(/,$/, '');
            str = `<div class="ui segment subservice" style="display: none;" id="subservice_`+idx+`">
                    <h2 class="ui floated header">
                        <span class="left floated">`+globalFrontendText["app_sub_service"]+` `+idx+` </span>
                        <span class="right floated"><i class="brown x icon link" onClick="removeSubservice(`+idx+`)"></i></span>
                    </h2>
                    <div class="field">
                    <label>`+globalFrontendText["git_path"]+`</label>
                    <div class="ui action input">
                        <input type="text" id="service_git_path_`+idx+`" value="`+service.git_path+`">
                        <button class="purple ui button ai_analyze_service_btn" onClick="analyzeService(`+idx+`)" value="1"><span id="ai_analyze_service_icon"><i class=" reddit square icon"></i></span>`+globalFrontendText["ai_code_analysis"]+`</button>
                    </div>
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_name"]+`</label>
                    <input type="text" id="service_name_`+idx+`" value="`+service.name+`">
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_type"]+`</label>
                    <select class="ui fluid dropdown" id="service_service_type_`+idx+`" value=`+service.service_type+`>
                        <option value="FRONTEND">前端/移动端（Frontend/Mobile）</option>
                        <option value="FRONTEND_BACKEND">前端+后端（Frontend + Backend）</option>
                        <option value="BACKEND">后端服务（Backend）</option>
                        <option value="GAME">游戏（GAME）</option>
                        <option value="COMMON">其它（Others）</option>
                    </select>
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_role"]+`</label>
                    <textarea id="service_role_`+idx+`" rows="4">`+service.role+`</textarea>
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_language"]+`</label>
                    <input type="text" id="service_language_`+idx+`" value="`+service.language+`">
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_framework"]+`</label>
                    <input type="text" id="service_framework_`+idx+`" value="`+service.framework+`">
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_libs"]+`</label>
                    <input type="text" id="service_libs_name_`+idx+`" value="`+libsStr+`">
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_api_type"]+`</label>
                    <input type="text" id="service_api_type_`+idx+`" value="`+service.api_type+`">
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_api_path"]+`</label>
                    <input type="text" id="service_api_location_`+idx+`" value="`+service.api_location+`">
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_database"]+`</label>
                    <input type="text" id="service_database_`+idx+`" value="`+service.database_type+`">
                    </div>
                    <div class="field">
                    <label>`+globalFrontendText["service_code_struct"]+`</label>
                    <textarea id="service_struct_cache_`+idx+`" rows="4">`+service.struct_cache+`</textarea>
                    </div>
                    <div class="field">
                    <label>CI - GitHub workflow</label>
                    <input type="text" id="service_workflow_`+idx+`" value="`+service.git_workflow+`">
                    </div>
                    <div class="field">
                    <label>CD - GROUP</label>
                    <input type="text" id="service_container_group_`+idx+`" value="`+service.cd_container_group+`">
                    </div>
                    <div class="field">
                    <label>CD - NAME</label>
                    <input type="text" id="service_container_name_`+idx+`" value="`+service.cd_container_name+`">
                    </div>
                    <div class="field">
                    <label>CD - REGION</label>
                    <input type="text" id="service_region_`+idx+`" value="`+service.cd_region+`">
                    </div>
                    <div class="field">
                    <label>CD - SECURITY GROUP</label>
                    <input type="text" id="service_security_group_`+idx+`" value="`+service.cd_security_group+`">
                    </div>
                    <div class="field">
                    <label>CD - SUBNET/SWITCH</label>
                    <input type="text" id="service_cd_subnet_`+idx+`" value="`+service.cd_subnet+`">
                    </div>

                    <div class="field">
                    <label>CD - SUBNET2(AWS)</label>
                    <input type="text" id="service_cd_subnet2_`+idx+`" value="`+service.cd_subnet2+`">
                    </div>
                    <div class="field">
                    <label>CD - VPC(AWS)</label>
                    <input type="text" id="service_cd_vpc_`+idx+`" value="`+service.cd_vpc+`">
                    </div>
                    <div class="field">
                    <label>CD - role_arn(AWS)</label>
                    <input type="text" id="service_cd_execution_role_arn_`+idx+`" value="`+service.cd_execution_role_arn+`">
                    </div>
                </div>
            </div>`
            $("#add-service").after(str)
            $("#subservice_"+idx).slideDown("500")
            setTimeout(function () {
                $('#app-edit').modal('refresh');
            }, 550);
            $("#service_service_type_"+idx).val(service.service_type)
        });
    }

    sendAjaxRequest('/app/get', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function analyzeService(elementID) {
    $("#ai_analyze_service_icon").html('<i class="loading spinner icon"></i>')
    $(".ai_analyze_service_btn").addClass("disabled")
    $('#app-edit').dimmer('show');

    var requestData = JSON.stringify({ 'service_git_path': $("#service_git_path_"+elementID).val() })

    successCallback = function(data) {
        data = data.data
        $("#ai_analyze_service_icon").html('<i class=" reddit square icon"></i>')
        $(".ai_analyze_service_btn").removeClass("disabled")
        $('#app-edit').dimmer('hide');
        console.log(data)
        console.log(elementID)
        $("#service_name_"+elementID).val(data.name)
        $("#service_service_type_"+elementID).val(data.service_type)
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
        $("#service_security_group_"+elementID).val(data.cd_security_group)
        $("#service_cd_subnet_"+elementID).val(data.cd_subnet)

        if ($("#app_name").val().length < 1) {
            $("#app_name").val(data.name)
        }
        if ($("#app_description").val().length < 1) {
            $("#app_description").val(data.role)
        }
        if ($("#app_default_source_branch").val().length < 1) {
            $("#app_default_source_branch").val('master')
            $("#app_default_target_branch").val('feat/xxx')
        }
    }

    errorCallback = function(data) {
        $("#ai_analyze_service_icon").html('<i class=" reddit square icon"></i>')
        $(".ai_analyze_service_btn").removeClass("disabled")
        $('#app-edit').dimmer('hide');
        setTimeout(function () {
            myAlert("ERROR", data)
        }, 1000);
    }

    sendAjaxRequest('/app/analyze_service', 'POST', requestData, successCallback, errorCallback, true, false)
}

function getAppTplList() {
    $("#tpl_select").empty();

    requestData = ''

    successCallback = function(data) {
        apps = data.data.apps
        console.log(apps)

        apps.forEach(function (app, element_index, element_array) {
            var newOption = $("<option></option>").attr("value", app.app_id).text(app.name);
            $("#tpl_select").append(newOption);
        });
    }

    sendAjaxRequest('/app/get_tpl', 'GET', requestData, successCallback, alertErrorCallback, true, false)
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
            str+= `
            <div class="item padding-15-0">
                <div class="content font-size-15 line-height-24">
                <a href="#" class="header font-size-19" onClick="showApp(`+app["app_id"]+`)">`+app["name"]+`</a>
                <div class="description font-color-gray">`+app["description"]+`</div>
                <div><i class="code branch purple icon"></i>`+globalFrontendText['app_base_branch']+`: `+app["default_source_branch"]+` <i class="angle right icon"></i> `+globalFrontendText['app_feat_branch']+`: `+app["default_target_branch"]+`</div>
            `
            services.forEach(function (service, element_index, element_array) {
                str += `
                <div>
                    <i class="circle icon tiny teal padding-right-16"></i>`+service["name"]+`
                    <i class="code icon  brown"></i>`+service["language"]+`
                    <i class="gavel icon  brown"></i>`+service["framework"]+`
                    <span class="description font-color-gray padding-left-20">`+service["role"]+`</span>
                </div>
                `
            });
            str += ` </div> </div>`
            $("#app_list").html(str)
        });
    }

    sendAjaxRequest('/app/get', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function rendSelect() {
    $("#app_git_config").empty();
    $("#app_ci_config").empty();
    $("#app_cd_config").empty();
    
    gitconfigs.forEach(function (gc, idx, arr) {
        var newOption = $("<option></option>").attr("value", gc.git_config_id).text(gc.name);
        

        if (idx == arr.length - 1) {

            newOption.prop("selected", true);
        }
        $("#app_git_config").append(newOption);
    })
    ciconfigs.forEach(function (gc, idx, arr) {
        var newOption = $("<option></option>").attr("value", gc.ci_config_id).text(gc.name);
        $("#app_ci_config").append(newOption);

        if (idx === arr.length - 1) {
            newOption.prop("selected", true);
        }
    })
    cdconfigs.forEach(function (gc, idx, arr) {
        var newOption = $("<option></option>").attr("value", gc.cd_config_id).text(gc.name);
        $("#app_cd_config").append(newOption);

        if (idx === arr.length - 1) {
            newOption.prop("selected", true);
        }
    })
}

function cleanUpApp() {
    $('.subservice').remove();
    $("#app_id").val('')
    $("#app_default_source_branch").val('')
    $("#app_default_target_branch").val('')
    $("#app_description").val('')
    $("#app_name").val('')
    $("#app_git_config").empty();
    $("#app_ci_config").empty();
    $("#app_cd_config").empty();
}


function getAction() {
    var queryString = window.location.search;

    var params = new URLSearchParams(queryString);

    var action = params.get('action');

    return action
}

function clickAddApplication() {
    action = ""
}