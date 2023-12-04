var globalTenantID = 0
var globalContext = []
var globalTasks = []
var gloablCode = {}
var globalFrontendText = {}
var globalCompileTimes = {}
var globalChangeServiceList = []
var globalDockerImage = ""
var globalRole = ""
var globalAppInfo = {}
var codeMirror
var apiUrl = "http://127.0.0.1:8081"

var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?b4ab6a8ab861f8cca03710ba96cb53c7";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();

function sendAjaxRequest(url, method, requestData, successCallback, errorCallback, async, slideDown) {       
    $.ajax({
        type: method,
        data: requestData,
        async: async,
        xhrFields: {
            withCredentials: true
        },
        url: apiUrl + url,
        contentType: 'application/json',
        dataType: 'json'
    }).done(data => {
        if (slideDown) {
            setTimeout(function () {
                $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
            }, 1000);
        }

        if( data.success ) {
            try {
                successCallback(data);
            } catch (error) {
                try {
                    errorCallback(data.error);
                    console.error(error);
                } catch (error) {
                    myAlert("ERROR", error);
                    console.error(error);
                }
            }
        } else {
            console.log(data.error)
            try {
                errorCallback(data.error, data);
            } catch (error) {
                myAlert("ERROR", error);
                console.error(error);
            }
        }
    }).fail(function () {
        errorMsg = "Network request exception."
        try {
            errorCallback(errorMsg + "<br />" + globalFrontendText["backend_return_error"]);
        } catch (error) {
            console.error(error);
            myAlert("ERROR", error);
        }
    });
}  

var aiErrorCallback = function (error){
    str = error
    $(".ai-code").eq($('ai-code').length - 1).html(str);
    $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    setTimeout(function () {
        $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
    }, 1000);
}

var alertErrorCallback = function(error) {
    if (typeof error === 'undefined') {
        error = "Unknown error"
    }
    myAlert("ERROR", error)
}

function getRoleImg(role_img, role) {
    if (role=="QA") {
        role_img = '<img class="ui avatar image" src="./static/image/role_qa.jpeg" data-content="QA" style="width: auto;height: auto;">'
    }
    if (role=="OP") {
        role_img = '<img class="ui avatar image" src="./static/image/role_op.jpeg" data-content="OP" style="width: auto;height: auto;">'
    }
    if (role=="PM") {
        role_img = '<img class="ui avatar image" src="./static/image/role_pm.jpeg" data-content="PM" style="width: auto;height: auto;">'
    }
    if (role=="TL") {
        role_img = '<img class="ui avatar image" src="./static/image/role_tl.jpeg"  data-content="TL"  style="width: auto;height: auto;">'
    }
    return role_img
}


function thinkUI(customPrompt, thinkText, role) {
    uuid = Math.random().toString(36).substr(2, 9) + Date.now().toString();

    role_img = getRoleImg('<i class="blue  grav icon big" style="font-size: 3em;"></i>', role)
    query_img = getRoleImg('<i class="blue  grav icon big" style="font-size: 3em;"></i>', globalRole)
    globalRole = ""
    
    $('#prompt-textarea').val("");
    $("#prompt-hidePrompt").val("")
    var newField = $('<div class="user-code-container"><div class="ui container grid"><div class="one wide column">'+query_img+'</div><div class="fifteen wide column ai-content"><div class="ai-code">' + marked.marked(customPrompt).replaceAll("\n", "<br />") + '</div></div></div></div> <div class="ai-code-container"><div class="ui container grid"><div class="one wide column">'+role_img+'</div><div class="fifteen wide column ai-content"><div class="ai-code '+uuid+'"><i class="spinner loading icon"></i>'+thinkText+'</div></div></div></div>');
    $(".ai-prompt-container").eq($('ai-prompt-container').length - 1).before(newField);
    $(".ai-code-container").eq($('ai-code-container').length - 1).hide();
    $(".user-code-container").eq($('user-code-container').length - 1).hide();
    setTimeout(function () {
        $(".user-code-container").eq($('user-code-container').length - 1).slideDown();
    }, 200);
    setTimeout(function () {
        $(".ai-code-container").eq($('ai-code-container').length - 1).slideDown();
    }, 700);
    setTimeout(function () {
        $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
    }, 900);
    $('img').popup();

    return uuid
}

function thinkUIShow(customPrompt, thinkText, role, role_two, service_name) {
    role_img = getRoleImg('<i class="blue  grav icon big" style="font-size: 3em;"></i>', role)
    if (!role_two) {
        role_two = ""
    }
    role_two_img = getRoleImg('<i class="blue  grav icon big" style="font-size: 3em;"></i>', role_two)

    customPrompt = customPrompt.replaceAll('\n\n', '\n')

    if (!service_name) {
        service_name = ""
    }
    var ai_code_class = service_name.replace("/","-")
    
    $('#prompt-textarea').val("");
    $("#prompt-hidePrompt").val("")
    var newField = $('<div class="user-code-container"><div class="ui container grid"><div class="one wide column">'+role_two_img+'</div><div class="fifteen wide column ai-content"><div class="ai-code">' + marked.marked(customPrompt) + '</div></div></div></div> <div class="ai-code-container"><div class="ui container grid"><div class="one wide column">'+role_img+'</div><div class="fifteen wide column ai-content"><div class="ai-code '+ai_code_class+'"><i class="spinner loading icon"></i>'+thinkText+'</div></div></div></div>');
    $(".ai-prompt-container").eq($('ai-prompt-container').length - 1).before(newField);

    $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
    $('img').popup();
}

function answerUI(str) {
    $(".ai-code").eq($('ai-code').length - 1).html(str);
    $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    setTimeout(function () {
        $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
    }, 1000);
}

function modelInfoUpdate(appName, content) {
    requestData = JSON.stringify({ "app_name": appName, "content": content })

    successCallback = function(data){
        $('#model-edit').modal('hide');
    }

    sendAjaxRequest('/app/update', 'POST', requestData, successCallback, alertErrorCallback, true, false)
}

modelSelectedSuccessCallback = function(data){
    data = data.data
    globalAppInfo = data
    var repos = ""
    data.app.service.forEach(function (s, element_index, element_array) {
        repos += '<i class="git square icon teal"></i>'+s.git_path+"<br/>"+s.name+": "+s.role+"<br/>"+s.struct_cache.replaceAll('\n', "<br/>").replaceAll('  ', "- ")+"<br/>"
    });
    str = '<i class="thumbtack icon teal"></i>'+globalFrontendText["ai_selected_app_2"] + ": "+ data["requirement_id"]
        +"<hr />"+'<i class="app store ios icon teal"></i>'+ data.app.name + ": " + data.app.description
        +"<hr />"+ repos
        +"<hr />"+'<i class="code branch teal icon"></i>'+ globalFrontendText["ai_selected_app_4"] + data.default_source_branch +" "+ globalFrontendText["ai_selected_app_5"] +" "+ data.default_target_branch
        +"<hr /><br />" + globalFrontendText["ai_selected_app_6"];
    goodcase = `<div class="ui middle aligned divided list goodcase_list">
    <h4 style="padding-top: 10px;">`+globalFrontendText["ai_goodcase_intro"]+`</h4>
    <div class="item">
      <div class="right floated content">
        <div class="ui button" onclick="useGoodCase('f_goodcase_content_1')">`+globalFrontendText["goodcase_chose"]+`</div>
      </div>
      <div class="content">
        <div class="header">`+globalFrontendText["goodcase_title_1"]+`</div>
        <span class="f_goodcase_content_1">`+globalFrontendText["goodcase_content_1"]+`</span>
      </div>
    </div>
    <div class="item">
      <div class="right floated content">
        <div class="ui button" onclick="useGoodCase('f_goodcase_content_2')">`+globalFrontendText["goodcase_chose"]+`</div>
      </div>
      <div class="content">
        <div class="header">`+globalFrontendText["goodcase_title_2"]+`</div>
        <span class="f_goodcase_content_2">`+globalFrontendText["goodcase_content_2"]+`</span>
      </div>
    </div>
    <div class="item">
      <div class="right floated content">
        <div class="ui button" onclick="useGoodCase('f_goodcase_content_3')">`+globalFrontendText["goodcase_chose"]+`</div>
      </div>
      <div class="content">
        <div class="header">`+globalFrontendText["goodcase_title_3"]+`</div>
        <span class="f_goodcase_content_3">`+globalFrontendText["goodcase_content_3"]+`</span>
      </div>
    </div>
    <div class="item">
      <div class="right floated content">
        <div class="ui button" onclick="useGoodCase('f_goodcase_content_4')">`+globalFrontendText["goodcase_chose"]+`</div>
      </div>
      <div class="content">
        <div class="header">`+globalFrontendText["goodcase_title_4"]+`</div>
        <span class="f_goodcase_content_4">`+globalFrontendText["goodcase_content_4"]+`</span>
      </div>
    </div>
  </div>`
    const url = window.location;
    const newUrl = url.origin + '/task.html?task_id=' + data["requirement_id"];
    history.pushState('', '', newUrl); 
    answerUI(str+goodcase)

    $(".ai-prompt-area").show()
}

function modelSelected(appName, appID, source_branch, feature_branch) {
    if (source_branch.length < 2 && feature_branch.length < 2) {
        source_branch = $("#model_source_branch_" + appID).val()
        feature_branch = $("#model_feature_branch_" + appID).val()
    }
    customPrompt = globalFrontendText["ai_select_app"] + ": " + appName
    $('.model-selector').addClass("disabled")
    $("#generate-code-button").removeClass("disabled")
    $('#model-modal').modal('hide');

    thinkUI(customPrompt, globalFrontendText["ai_think"], "PM")

    requestData = JSON.stringify({ "app_id": appID, "source_branch": source_branch, "feature_branch": feature_branch })

    errorCallback = function (error){
        $('.model-selector').removeClass("disabled")
        str = error
        $(".ai-code").eq($('ai-code').length - 1).html(str);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
        setTimeout(function () {
            $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
        }, 1000);
    }

    sendAjaxRequest('/requirement/setup_app', 'POST', requestData, modelSelectedSuccessCallback, errorCallback, true, true)
}

$(document).ready(function () {
    language()
    showUrlErrorMsg()

    const url = window.location;
    const path = url.pathname;
    if (path != "/index.html" && path != "/" && path != "/i_clouderwork.html") {
        logincheck()
        getRequirement()
    }

    var p_app_id = getUrlParams("app_id")
    var p_branch = getUrlParams("branch")
    var p_app_name = getUrlParams("app_name")
    if (p_app_id>0 && p_branch.length>2 && p_app_name.length>2) {
        modelSelected(p_app_name, p_app_id, p_branch, p_branch)
    }

    $('img').popup();

    codeMirror = CodeMirror.fromTextArea(document.getElementById('code-edit-code'), {
      theme: 'darcula',
      mode: 'haxe', 
      lineNumbers: true 
    });

    $('.model-selector').click(function () {
        successCallback = function(data) {
            var str = ''
            data.data.apps.forEach(function (app, element_index, element_array) {
                var repos = ""
                app.service.forEach(function (service) {
                    repos += service["name"]+", "
                })
                repos = repos.replace(/, $/g, '')

                var rand = Math.random().toString(36).substr(2, 4)
                feature_branch = app.default_target_branch +'/'+ getCurrentDate()+'_'+rand

                str += `
                    <div class="item" style="padding: 15px 0px;">
                        <div class="content">
                        <div class="header" style="line-height: 25px;">
                            `+globalFrontendText["app"]+`: `+app.name+`
                            <br />
                            `+globalFrontendText["ai_selected_app_4"]+`
                            <input type="text" placeholder="" value="`+app.default_source_branch+`" class="fenzhiguifan" id="model_source_branch_`+app.app_id+`">
                            `+globalFrontendText["ai_selected_app_5"]+`
                            <input type="text" placeholder="" value="`+feature_branch+`" class="fenzhiguifan" id="model_feature_branch_`+app.app_id+`">
                        </div>
                        <div class="description" style="line-height: 25px;">`+app.description+`</div>
                        <div class="ui button blue model-selected" onClick="modelSelected('`+app.name+`','`+app.app_id+`', '', '')" style="float: right;">`+globalFrontendText["start_task"]+`</div> 
                        </div>
                    </div>
                `
            })
            if (str.length < 1) {
                str = globalFrontendText["msg_empty_task"]
            }
            $(".model_list").html(str)
            $('#model-modal').modal('show');
        }

        sendAjaxRequest('/app/get', 'GET', "", successCallback, alertErrorCallback, true, false)
    });
    $('#model-cancel').click(function () {
        $('#model-modal').modal('hide');
    });

    // 修改模型
    $('#mode-edit-content-cancel').click(function () {
        $('#model-edit').modal('hide');
    });
    $('#mode-edit-content-save').click(function () {
        appName = $("#mode-edit-app-name").val()
        content = $("#mode-edit-content").val()
        modelInfoUpdate(appName, content)
    });

    // 提交任务
    $('#generate-code-button').click(function () {
        $('#generate-code-button').addClass("disabled");
        var customPrompt = $('#prompt-textarea').val();
        $('#prompt-textarea').val('');
        var operType = $('#prompt-hidePrompt').val();
        $('#prompt-hidePrompt').val('');
        var serviceName = $('#prompt-serviceName').val();
        $('#prompt-serviceName').val('');
        if (operType == "tec_doc") { 
            taskSplitOK(customPrompt, serviceName)
        } else if (operType == "api_doc") {
            globalChangeServiceList.forEach(function (element, element_index, element_array) {
                if (element_index > 0 ) {
                    setTimeout(function () {
                        taskAnalysis(customPrompt, element, true)
                    }, 200);
                } else {
                    taskAnalysis(customPrompt, element)
                }
            })
        } else if (operType == "requirement_doc") {
            if (globalChangeServiceList.length == 1) {
                taskAnalysis(customPrompt, globalChangeServiceList[0])
            } else {
                genInterfaceDoc(customPrompt)
            }
        } else {
            clarify(customPrompt)
        }
    });

    $('#cancel-task').click(function () {
        window.location.href = "/task.html"
    });

    // show dropdown on hover
    $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
    });

    // edit
    $("#code-actions-edit").click(function () {
        var uuid = $("#code-actions-uuid").val();
        var code = gloablCode["newCode_" + uuid];

        codeMirror.setValue(code);

        $("#model-edit-code").modal('show');
        setTimeout(function () {
          codeMirror.setValue(code);
        }, 800); 
    });
    $("#code-edit-use-old").click(function () {
        var uuid = $("#code-actions-uuid").val();
        var code = gloablCode["oldCode_" + uuid];
        $("#code-edit-code").val(code);
    });
    $("#code-edit-code-save").click(function () {
        var newcode = codeMirror.getValue();
        var uuid = $("#code-actions-uuid").val()
        gloablCode["newCode_" + uuid] = newcode
        compareCode(uuid)
    });
    $("#code-edit-code-cancel").click(function () {
        $("#model-edit-code").modal('hide');
    });

    $("#code-actions-cancel").click(function () {
        $("#model-diff").modal('hide');
    });

});

function getCurrentDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');
    
    return `${year}${month}${day}`;
  }

function escapeString(str) {
    console.log("str:"+str)
    if (typeof str === 'undefined') {
        return ""
    }
    return str.replace(/[\\'"\r\n\t\b\f\v]/g, function(match) {
      switch (match) {
        case '\\':
          return '\\\\'; 
        case '\'':
          return '\\\''; 
        case '\"':
          return '\\"'; 
        case '\f':
          return '\\f'; 
        case '\v':
          return '\\v'; 
        default:
          return match; 
      }
    });
  }

function getRequirement() {
    var requirement_id = getTaskID()
    info = { 'requirement_id': requirement_id }

    successCallback = function(data) {
        modelSelectedSuccessCallback(data)
        for (let element_index = 0; element_index < data.data.memory.length; element_index++) {
            const memory = data.data.memory[element_index];
            
            console.log(memory);
            
            if (memory.artifact_type == "RequirementDocument") {
                role_two = ''
                if (memory.step == "Requirement_adjust") { 
                    role_two = "TL"
                }
                thinkUIShow(memory.input_prompt, globalFrontendText["ai_think"], 'PM', role_two);
                const d = {
                    "data": {
                        "message": JSON.parse(memory.artifact_content),
                        "input_prompt": memory.input_prompt
                    }
                };
                clarifySuccessCallback(d, true);
            }
            if (memory.step == "API_organize") {
                thinkUIShow(memory.artifact_type, globalFrontendText["ai_think"], 'TL');
                const d = {
                    "data": {
                        "message": memory.artifact_content
                    }
                };
                genInterfaceDocSuccessCallback(d);
            }
            if (memory.step == "Subtask_subtasks") {
                thinkUIShow(memory.artifact_path, globalFrontendText["ai_think"], 'TL', '', memory.artifact_path);
                const d = {
                    "data": {
                        "message": memory.artifact_content,
                        "service_name": memory.artifact_path
                    }
                };
                taskAnalysisSuccessCallback(d, true);
            }
            if (memory.step == "Subtask_code") {
                thinkUIShow(memory.artifact_path, globalFrontendText["ai_think"], 'TL', '', memory.artifact_path);
                const info = {
                        "files": JSON.parse(memory.artifact_content),
                        "service_name": memory.artifact_path
                    };
                pluginTaskList(info, true)
            }
            if (memory.step == "Code_checkCode") {
                codedata = {
                    "data": {
                        code: memory.artifact_content,
                        reasoning: memory.input_prompt,
                        success: true
                    }
                }
                uuid = 0
                service_name = ""
                for (const key in globalTasks) {
                    globalTasks[key].forEach(function (file, element_index, element_array) {
                        let file_path = file["file-path"]
                        if (file_path.endsWith(memory.artifact_path)) {
                            uuid = file.uuid
                            service_name = key
                        }
                    })
                }
                checkCodeStar(uuid, service_name)
                checkCodeSuccessCallback(codedata, uuid, memory.artifact_path)
            }
            if (memory.step == "Code_fixError_compile") {
                codedata = {
                    "data": JSON.parse(memory.artifact_content)
                }
                uuid = 0
                service_name = ""
                for (const key in globalTasks) {
                    globalTasks[key].forEach(function (file, element_index, element_array) {
                        let file_path = file["file-path"]
                        if (file_path == memory.artifact_path) {
                            uuid = file.uuid
                            service_name = key
                        }
                    })
                }
                fixCompileStar(service_name, element_index, uuid)
                fixCompileSuccessCallback(codedata, service_name, element_index, uuid, memory.artifact_path)
            }
            if (memory.step == "Code_fixError_lint") {
                codedata = {
                    "data": JSON.parse(memory.artifact_content)
                }
                uuid = 0
                service_name = ""
                for (const key in globalTasks) {
                    globalTasks[key].forEach(function (file, element_index, element_array) {
                        let file_path = file["file-path"]
                        if (file_path == memory.artifact_path) {
                            uuid = file.uuid
                            service_name = key
                        }
                    })
                }
                fixLintStar(service_name, element_index, uuid)
                fixLintSuccessCallback(codedata, service_name, element_index, uuid, memory.artifact_path)
            }
            if (memory.step == "DevOps_CI") {
                if (memory.artifact_content.length > 0 ) {
                    uuid = thinkUI(memory.step, globalFrontendText["ai_think"], 'QA');
                    try {
                        const info = JSON.parse(memory.artifact_content.replaceAll("'", '"'))
                        pluginci(info, uuid)
                    } catch (error) {
    
                    }
                }
            }
            if (memory.step == "DevOps_CD") {
                setTimeout(function () {
                    thinkUI(memory.step, globalFrontendText["ai_think"], 'OP');
                    const d = {
                        "data": {
                            "internet_ip": memory.artifact_content,
                        }
                    };
                    startCDsuccessCallback(d, true);
                }, 1000);
                
            }
        }        
    }

    errorCallback = function(data){
        myAlertPure(globalFrontendText["notice"], data +'<hr />'+ globalFrontendText["opensource_version_1"] + ": ./workspace/"+requirement_id)
    }

    if (requirement_id>0) {
        sendAjaxRequest('/requirement/get_one', 'GET', info, successCallback, errorCallback, true, false)
    }
}

function genCodeCallbackPushcode(isSuccess, data) {
    var uuid = data.plugin.uuid;
    if (isSuccess) {
        $("#task_status_push_"+uuid).addClass("green")
        $("#task_status_push_"+uuid).removeClass("olive")
        $("#task_status_push_" + uuid).html(`<i class="check icon"></i> `+globalFrontendText["submit"])
    } else {
        $("#task_status_push_"+uuid).addClass("red")
        $("#task_status_push_"+uuid).removeClass("olive")
        $("#task_status_push_" + uuid).html(`<i class="times icon"></i> `+globalFrontendText["submit"])
    }
}

function language() {
    successCallback = function(data) {
        var frontendText = data.data.frontend_text
        globalFrontendText = frontendText
        for (const key in frontendText) {
            if (frontendText.hasOwnProperty(key)) {
              const value = frontendText[key];
              console.log(key + ": " + value);
              $(".f_"+key).html(value)
            }
        }
    }

    errorCallback = function(data) {
        console.log(data)
        $("#my-login").modal('show')
        myAlertPure("Error 错误", "The back-end service interface cannot be accessed. Please check the terminal service log and browser console. (Usually the back-end service is not started, Or exists <a href='https://github.com/kuafuai/DevOpsGPT/blob/master/docs/DOCUMENT.md#configuration-details' target='_blank'> Cross-domain problem? </a>)<br /><br />无法访问后端服务接口，请检查终端服务日志以及浏览器控制台报错信息。（通常是后端服务没有启动，或存在 <a href='https://github.com/kuafuai/DevOpsGPT/blob/master/docs/DOCUMENT_CN.md#%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E7%B1%BB' target='_blank'>跨域问题？</a>）")
    }

    sendAjaxRequest('/user/language', 'GET', "", successCallback, errorCallback, false, false)
}

function openUrl(newurl){
    window.location.href = newurl;
}

function openUrlNew(newurl){
   window.open(newurl);
}

function logincheck() {
    const url = window.location;
    const path = url.pathname;

    info = { 'requirement_id': getTaskID(), "url_path": path }

    successCallback = function(data) {
        var username = data.data.username
        var tenant = data.data.tenant_name
        var code_power = data.data.code_power
        globalTenantID = data.data.tenant_id
        $("#current-username").html(username)
        $("#current-tenant").html(tenant+' ('+data.data.billing_type_name+" | "+globalFrontendText['code_power']+':'+code_power+')')
        $("#watermark-username").html(username)
    }

    errorCallback = function(msg, data) {
        console.log("111111", data)
        if (data.code == 401) {
            username = "Guest"
            $("#current-username").html(username)
            $("#watermark-username").html(username)
            if (path != "/user_login.html" && path != "/user_register.html" && path != "/user_changepassword.html") {
                window.location.href = "user_login.html";
            }        
        } else if (data.code == 404) {
            myAlert(globalFrontendText["notice"], msg)
        }
    }

    sendAjaxRequest('/requirement/clear_up', 'GET', info, successCallback, errorCallback, false, false)
}

function logout() {
    successCallback = function() {
        window.location.href = "user_login.html";
    }

    sendAjaxRequest('/user/logout', "GET", "", successCallback, alertErrorCallback, false, true)
}

function changeLanguage() {
    successCallback = function() {
        location.reload();
    }

    sendAjaxRequest('/user/change_language', "GET", "", successCallback, alertErrorCallback, true, false)
}



function myAlert(alert_title, alert_content) {
    $("#my-alert-title").html(alert_title)
    $("#my-alert-content").html(convertURLsToLinks(alert_content))
    $("#my-alert").modal('show')
}

function myAlertPure(alert_title, alert_content) {
    $("#my-alert-title").html(alert_title)
    $("#my-alert-content").html(alert_content)
    $("#my-alert").modal('show')
}

function showCode(element) {
    $("#my-alert-title").html($(element).attr("show-code-key"))
    $("#my-alert-content").html("<h4>"+decodeURI($(element).attr("show-code-reason"))+"</h4><pre>"+decodeURI($(element).attr("show-code-value"))+"</pre>")
    $("#my-alert").modal('show')
}

function getParameterByName(name) {
    name = name.replace(/[\[\]]/g, "\\$&");
    var url = window.location.href;
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    var results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function triggerPlugin(plugin) {
    console.log(plugin)
    if (plugin["name"] == "ci") {
        pluginci(plugin["info"])
    }
    if (plugin["name"] == "task_list") {
        pluginTaskList(plugin["info"], false)
    }
    if (plugin["name"] == "task_runner") {
        pluginTaskRunner(plugin["info"])
    }
}

function pluginTaskRunner(info) {
    if (info["status"] == "已失败") {
        $("#task_status_redo_"+info["front_uuid"]).children().removeClass("spinner")
        $("#task_status_redo_"+info["front_uuid"]).children().removeClass("loading")
        $("#task_status_redo_"+info["front_uuid"]).children().addClass("close")
        $("#task_status_redo_"+info["front_uuid"]).addClass("red")
        $("#task_status_redo_"+info["front_uuid"]).removeClass("olive")
        $("#task_status_redo_"+info["front_uuid"]).attr("show-code-key", info["file_path"])
        $("#task_status_redo_"+info["front_uuid"]).attr("show-code-value", escapeHtml(info["newCode"]))
    } else {
        $("#task_status_redo_"+info["front_uuid"]).children().removeClass("spinner")
        $("#task_status_redo_"+info["front_uuid"]).children().removeClass("loading")
        $("#task_status_redo_"+info["front_uuid"]).children().addClass("check")
        $("#task_status_redo_"+info["front_uuid"]).addClass("green")
        $("#task_status_redo_"+info["front_uuid"]).removeClass("olive")
        $("#task_status_redo_"+info["front_uuid"]).attr("show-code-key", info["file_path"])
        $("#task_status_redo_"+info["front_uuid"]).attr("show-code-reason", escapeHtml(info["reasoning"]))
        $("#task_status_redo_"+info["front_uuid"]).attr("show-code-value", escapeHtml(info["newCode"]))

        checkCode(info["newCode"], info["file_task"], info["front_uuid"], info["file_path"], info["repo_path"])
    }
    gloablCode["newCode_" + info["front_uuid"]] = info["newCode"]
    gloablCode["oldCode_" + info["front_uuid"]] = info["oldCode"]
}

function createWS(serviceName) {
    $("#my-alert").modal('hide')
    var requestData = JSON.stringify({ 'repo_path': serviceName, 'task_id': getTaskID() })

    successCallback = function(data){}

    errorCallback = function(error) {
        var retruBtn = '<br /><br /><button class="ui green button" onClick="createWS(\''+serviceName+'\')">'+globalFrontendText["retry"]+'</button>'
        myAlertPure("ERROR", error + retruBtn)
        throw new Error("发生了一个错误")
    }

    sendAjaxRequest('/workspace/create', "POST", requestData, successCallback, errorCallback, false, false)
}

function fixLintStar(service_name, times, uuid){
    let buttonid = "task_status_fix_lint_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_fix_lint_button tiny `+service_name.replace("/","-")+`" id="` + buttonid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["fix_static_scan"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_fix_lint_button').popup();
}

function fixLintSuccessCallback(data, service_name, times, uuid, file_path) {
    let buttonid = "task_status_fix_lint_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
    $("#"+buttonid).children().removeClass("spinner")
    $("#"+buttonid).children().removeClass("loading")
    $("#"+buttonid).children().addClass("check")
    $("#"+buttonid).addClass("green")
    $("#"+buttonid).removeClass("olive")
    $("#"+buttonid).attr("show-code-key", file_path)
    $("#"+buttonid).attr("show-code-value", escapeHtml(data.data["code"]))
    $("#"+buttonid).attr("show-code-reason", escapeHtml(data.data["reasoning"]))

    gloablCode["newCode_" + uuid] = data.data["code"]
}

function fixLint(error_msg, solution, uuid, file_path, service_name, times) {
    if (times >= 2) {
        return
    }
    var code = gloablCode["newCode_" + uuid]

    fixLintStar(service_name, times, uuid)

    var requestData = JSON.stringify({ 'code': code, 'error_msg': error_msg, 'solution': solution, 'task_id': getTaskID(), 'file_path': file_path })

    successCallback = function(data) {
        fixLintSuccessCallback(data, service_name, times, uuid, file_path)

        times++
        checkLint(service_name, file_path, uuid, times)
    }

    errorCallback = function(error) {
        let buttonid = "task_status_fix_lint_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
        $("#"+buttonid).children().removeClass("spinner")
        $("#"+buttonid).children().removeClass("loading")
        $("#"+buttonid).children().addClass("close")
        $("#"+buttonid).addClass("red")
        $("#"+buttonid).removeClass("olive")
        $("#"+buttonid).attr("show-code-key", file_path)
        $("#"+buttonid).attr("show-code-value", "")
    }

    sendAjaxRequest('/step_code/fix_lint', "POST", requestData, successCallback, errorCallback, true, false)
}

function fixCompileSuccessCallback(data, service_name, times, uuid, file_path) {
    let buttonid = "task_status_fix_compile_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
    $("#"+buttonid).children().removeClass("spinner")
    $("#"+buttonid).children().removeClass("loading")
    $("#"+buttonid).children().addClass("check")
    $("#"+buttonid).addClass("green")
    $("#"+buttonid).removeClass("olive")
    $("#"+buttonid).attr("show-code-key", file_path)
    $("#"+buttonid).attr("show-code-value", escapeHtml(data.data["code"]))
    $("#"+buttonid).attr("show-code-reason", escapeHtml(data.data["reasoning"]))

    gloablCode["newCode_" + uuid] = data.data["code"]
}

function fixCompileStar(service_name, times, uuid) {
    let buttonid = "task_status_fix_compile_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_fix_compile_button tiny `+service_name.replace("/","-")+`" id="` + buttonid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["fix_compile_check"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_fix_compile_button').popup();
}

function fixCompile(error_msg, solution, uuid, file_path, service_name, times) {
    if (times >= 2) {
        return
    }
    var code = gloablCode["newCode_" + uuid]

    fixCompileStar(service_name, times, uuid)

    var requestData = JSON.stringify({ 'code': code, 'solution': solution, 'task_id': getTaskID(), 'file_path': file_path, 'error_msg': error_msg })
    
    successCallback = function(data) {
        fixCompileSuccessCallback(data, service_name, times, uuid, file_path)

        times++
        checkCompile(service_name, times)
    }

    errorCallback = function(error) {
        let buttonid = "task_status_fix_compile_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
        $("#"+buttonid).children().removeClass("spinner")
        $("#"+buttonid).children().removeClass("loading")
        $("#"+buttonid).children().addClass("close")
        $("#"+buttonid).addClass("red")
        $("#"+buttonid).removeClass("olive")
        $("#"+buttonid).attr("show-code-key", file_path)
        $("#"+buttonid).attr("show-code-value", "")
    }
    
    sendAjaxRequest('/step_code/fix_compile', "POST", requestData, successCallback, errorCallback, true, false)
}

function saveCode(service_name, filePath, uuid) {
    var code = gloablCode["newCode_" + uuid]
    var requestData = JSON.stringify({ 'service_name': service_name, 'file_path': filePath, "code": code, 'task_id': getTaskID() })

    successCallback = function(){}

    sendAjaxRequest('/workspace/save_code', "POST", requestData, successCallback, alertErrorCallback, false, false)
}

function checkLint(service_name, filePath, uuid, times) {
    saveCode(service_name, filePath, uuid)
    
    let buttonid = "task_status_check_lint_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid

    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_check_lint_button tiny `+service_name.replace("/","-")+`" id="` + buttonid + `" data-content="点击查看代码" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["static_scan"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_check_lint_button').popup();

    var requestData = JSON.stringify({ 'service_name': service_name, 'file_path': filePath, 'task_id': getTaskID() })

    successCallback = function(data) {
        if (data.data["pass"] == false) {
            $("#"+buttonid).children().removeClass("spinner")
            $("#"+buttonid).children().removeClass("loading")
            $("#"+buttonid).children().addClass("close")
            $("#"+buttonid).addClass("red")
            $("#"+buttonid).removeClass("olive")
            $("#"+buttonid).attr("show-code-key", globalFrontendText["static_scan"]+": "+filePath)
            $("#"+buttonid).attr("show-code-reason", "Not pass")
            $("#"+buttonid).attr("show-code-value", escapeHtml(data.data["message"]))
            fixLint(data.data["message"], data.data["reasoning"][0]["solution-analysis"], uuid, filePath, service_name, times)
        } else {
            $("#"+buttonid).children().removeClass("spinner")
            $("#"+buttonid).children().removeClass("loading")
            $("#"+buttonid).children().addClass("check")
            $("#"+buttonid).addClass("green")
            $("#"+buttonid).removeClass("olive")
            $("#"+buttonid).attr("show-code-reason", "Pass")
            $("#"+buttonid).attr("show-code-key", globalFrontendText["static_scan"]+": "+filePath)
            $("#"+buttonid).attr("show-code-value", escapeHtml(data.data["message"]))
        }
    }

    errorCallback = function(error) {
        $("#"+buttonid).children().removeClass("spinner")
        $("#"+buttonid).children().removeClass("loading")
        $("#"+buttonid).children().addClass("close")
        $("#"+buttonid).addClass("red")
        $("#"+buttonid).removeClass("olive")
        $("#"+buttonid).attr("show-code-reason", "Not pass "+error)
        $("#"+buttonid).attr("show-code-key", globalFrontendText["static_scan"] + ": "+filePath)
        $("#"+buttonid).attr("show-code-value", "Falied")
    }

    sendAjaxRequest('/step_devops/check_lint', "POST", requestData, successCallback, errorCallback, true, false)
}

function checkCodeStar(uuid, service_name) {
    str = $("#task_status_td_" + uuid).html()+`
    <button class="ui circular olive icon button task_status_check_button tiny `+service_name.replace("/","-")+`" id="task_status_check_` + uuid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["self_check"]+`</button>
    `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_button').popup();
}

function checkCodeSuccessCallback(data, uuid, file_path) {
    console.log("checkCodeSuccessCallback:", data, uuid, file_path)
    var elements = document.querySelectorAll('[id="task_status_check_'+uuid+'"]');
    console.log(elements)

    var i = elements.length-1
    $(elements[i]).children().removeClass("spinner")
    $(elements[i]).children().removeClass("loading")
    $(elements[i]).children().addClass("check")
    $(elements[i]).addClass("green")
    $(elements[i]).removeClass("olive")
    $(elements[i]).attr("show-code-key", file_path)
    $(elements[i]).attr("show-code-value", escapeHtml(data.data["code"]))
    $(elements[i]).attr("show-code-reason", escapeHtml(data.data["reasoning"]))

    gloablCode["newCode_" + uuid] = data.data["code"]
}

function checkCode(code, fileTask, uuid, file_path, service_name, step) {
    if (code.length < 1) {
        code = gloablCode["newCode_" + uuid]
    }
    checkCodeStar(uuid, service_name)

    var requestData = JSON.stringify({ 'code': code, 'fileTask': fileTask, 'task_id': getTaskID(), 'file_path': file_path, 'service_name': service_name, 'step': step })

    successCallback = function(data){
        checkCodeSuccessCallback(data, uuid, file_path)

        // 这里Java总会画蛇添足，改为手动触发
        review_btn = `<button class="ui circular blue icon button tiny `+service_name.replace("/","-")+`" data-content="" onClick="checkCode('', '`+escapeHtml(data.data["reasoning"])+`', '`+uuid+`', '`+file_path+`', '`+service_name+`')"> `+globalFrontendText["trigger_code_review"]+`</button>`
        var elements = document.querySelectorAll('[id="task_status_check_'+uuid+'"]');
        var i = elements.length-1
        $(elements[i]).after(review_btn)

        // 暂时改为手动去点检查
        // if(globalTasks[service_name.replace("/","-")].length == $('.'+service_name.replace("/","-")+'.green.task_status_check_button').length){
        //     checkCompile(service_name, 0)
        // }
    }

    errorCallback = function(error){
        $("#task_status_check_"+uuid).children().removeClass("spinner")
        $("#task_status_check_"+uuid).children().removeClass("loading")
        $("#task_status_check_"+uuid).children().addClass("close")
        $("#task_status_check_"+uuid).addClass("red")
        $("#task_status_check_"+uuid).removeClass("olive")
        $("#task_status_check_"+uuid).attr("show-code-key", file_path)
        $("#task_status_check_"+uuid).attr("show-code-value", code)
        $("#task_status_check_"+uuid).attr("show-code-reason", error)
    }

    sendAjaxRequest('/step_code/check_code', "POST", requestData, successCallback, errorCallback, true, false)
}

function checkCompileSuccessCallback(data, times, repo_path){
    if (data.data["pass"] == false) {
        globalTasks[repo_path.replace("/","-")].forEach(function (file, element_index, element_array) {
            let uuid = file.uuid
            let buttonid = "task_status_checkcompile_"+globalCompileTimes[repo_path.replace("/","-")]+"_"+times+"_"+uuid
            let file_path = file["file-path"]
            $("#"+buttonid).children().removeClass("spinner")
            $("#"+buttonid).children().removeClass("loading")
            $("#"+buttonid).children().addClass("close")
            $("#"+buttonid).removeClass("olive")
            $("#"+buttonid).attr("show-code-key", globalFrontendText["compile_check"])
            $("#"+buttonid).attr("show-code-value", escapeHtml(data.data["message"]))

            var solution = globalFrontendText["no_problem_this_file"]+"<br />"
            for (let element_index = 0; element_index < data.data["reasoning"].length; element_index++) {
                let element = data.data["reasoning"][element_index];
                if (element["file-path"].includes(file_path)) {
                    $("#"+buttonid).addClass("red")
                    solution = element["solution-analysis"];
                    fixCompile(data.data["message"], solution, uuid, file_path, repo_path, times)
                    break
                } else {
                    $("#"+buttonid).addClass("teal")
                    solution += "- "+element["solution-analysis"]+"<br />";
                }
            }
            $("#"+buttonid).attr("show-code-reason", solution)
        });

    } else {
        globalTasks[repo_path.replace("/","-")].forEach(function (file, element_index, element_array) {
            let uuid = file.uuid
            let buttonid = "task_status_checkcompile_"+globalCompileTimes[repo_path.replace("/","-")]+"_"+times+"_"+uuid
            $("#"+buttonid).children().removeClass("spinner")
            $("#"+buttonid).children().removeClass("loading")
            $("#"+buttonid).children().addClass("check")
            $("#"+buttonid).addClass("green")
            $("#"+buttonid).removeClass("olive")
            $("#"+buttonid).attr("show-code-reason", "PAAS")
            $("#"+buttonid).attr("show-code-key", globalFrontendText["compile_check"])
            $("#"+buttonid).attr("show-code-value", escapeHtml(data.data["message"]))
            checkLint(repo_path, file["file-path"], uuid, 0)
        });
    }
}

function checkCompile(repo_path, times) {
    if (typeof globalCompileTimes[repo_path.replace("/","-")] === 'undefined') {
        globalCompileTimes[repo_path.replace("/","-")] = 0
    } else {
        globalCompileTimes[repo_path.replace("/","-")]++ 
    }

    globalTasks[repo_path.replace("/","-")].forEach(function (file, element_index, element_array) {
        let uuid = file.uuid
        let file_path = file["file-path"]
        saveCode(repo_path, file_path, uuid)
    })

    globalTasks[repo_path.replace("/","-")].forEach(function (file, element_index, element_array) {
        let uuid = file.uuid
        let buttonid = "task_status_checkcompile_"+globalCompileTimes[repo_path.replace("/","-")]+"_"+times+"_"+uuid
        str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_button tiny" id="` + buttonid + `" onClick="showCode(this)" data-content=""><i class="spinner loading icon"></i> `+globalFrontendText["compile_check"]+`</button>
        `
        $("#task_status_td_" + uuid).html(str)
        $('.task_status_button').popup();
    });

    var requestData = JSON.stringify({ 'repo_path': repo_path, 'task_id': getTaskID() })

    successCallback = function(data) {
        checkCompileSuccessCallback(data, times, repo_path)
    }

    errorCallback = function(error){
        globalTasks[repo_path.replace("/","-")].forEach(function (file, element_index, element_array) {
            let uuid = file.uuid
            let buttonid = "task_status_checkcompile_"+globalCompileTimes[repo_path.replace("/","-")]+"_"+times+"_"+uuid
            $("#"+buttonid).children().removeClass("spinner")
            $("#"+buttonid).children().removeClass("loading")
            $("#"+buttonid).children().addClass("close")
            $("#"+buttonid).addClass("red")
            $("#"+buttonid).removeClass("olive")
            $("#"+buttonid).attr("data-content", error)
        });
    }

    sendAjaxRequest('/step_devops/check_compile', "POST", requestData, successCallback, errorCallback, true, false)
}

function editFileTask(service_name, file_idx) {
    console.log("editFileTask:", service_name, file_idx)

    var uuid = globalTasks[service_name.replace("/","-")][file_idx]["uuid"];
    var newCode = gloablCode["newCode_" + uuid]
    var fileTask = globalTasks[service_name.replace("/","-")][file_idx]["code-interpreter"]
    var newTask = globalTasks[service_name.replace("/","-")][file_idx]["code-edit-task"]
    var file_path = globalTasks[service_name.replace("/","-")][file_idx]["file-path"]

    // 如果没有输入修改建议，直接点击重启，则重新生成代码
    if (newTask==undefined || newTask.length < 1) {
        var oldCode = globalTasks[service_name.replace("/","-")][file_idx]["code"]
        var step = globalTasks[service_name.replace("/","-")][file_idx]["step"]
        return checkCode(oldCode, fileTask, uuid, file_path, service_name, step)
    }

    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_button tiny" id="task_status_redo_` + uuid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["initial_code"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_button').popup();

    var requestData = JSON.stringify({ 'file_task': fileTask, 'new_task': newTask, 'new_code': newCode, 'task_id': getTaskID(), 'file_path': file_path })

    successCallback = function(data){
        $("#task_status_redo_"+uuid).children().removeClass("spinner")
        $("#task_status_redo_"+uuid).children().removeClass("loading")
        $("#task_status_redo_"+uuid).children().addClass("check")
        $("#task_status_redo_"+uuid).addClass("green")
        $("#task_status_redo_"+uuid).removeClass("olive")
        $("#task_status_redo_"+uuid).attr("show-code-key", file_path)
        $("#task_status_redo_"+uuid).attr("show-code-value", escapeHtml(data.data["code"]))
        $("#task_status_redo_"+uuid).attr("show-code-reason", escapeHtml(data.data["reasoning"]))

        gloablCode["newCode_" + uuid] = data.data["code"]

        checkCode(data.data["code"], fileTask, uuid, file_path, service_name)
    }

    errorCallback = function(error){
        $("#task_status_redo_"+uuid).children().removeClass("spinner")
        $("#task_status_redo_"+uuid).children().removeClass("loading")
        $("#task_status_redo_"+uuid).children().addClass("close")
        $("#task_status_redo_"+uuid).addClass("red")
        $("#task_status_redo_"+uuid).removeClass("olive")
        $("#task_status_redo_"+uuid).attr("show-code-key", file_path)
        $("#task_status_redo_"+uuid).attr("show-code-value", error)
    }

    sendAjaxRequest('/step_code/edit_file_task', "POST", requestData, successCallback, errorCallback, true, false)
}

function mergeCode(uuid, newCode, oldCode, fileTask, service_name, file_path) {
    console.log("mergeCode:", uuid, newCode, oldCode)

    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_check_button tiny `+service_name.replace("/","-")+`" id="task_status_check_` + uuid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["self_check"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_button').popup();

    var requestData = JSON.stringify({ 'file_task': fileTask, 'new_code': newCode, 'old_code': oldCode, 'task_id': getTaskID(), 'file_path': file_path })

    successCallback = function(data) {
        $("#task_status_check_"+uuid).children().removeClass("spinner")
        $("#task_status_check_"+uuid).children().removeClass("loading")
        $("#task_status_check_"+uuid).children().addClass("check")
        $("#task_status_check_"+uuid).addClass("green")
        $("#task_status_check_"+uuid).removeClass("olive")
        $("#task_status_check_"+uuid).attr("show-code-key", file_path)
        $("#task_status_check_"+uuid).attr("show-code-value", escapeHtml(data.data["code"]))
        $("#task_status_check_"+uuid).attr("show-code-reason", escapeHtml(data.data["reasoning"]))

        gloablCode["newCode_" + uuid] = data.data["code"]

        // 暂时改为手动去点检查
        // if(globalTasks[service_name.replace("/","-")].length == $('.'+service_name.replace("/","-")+'.green.task_status_check_button').length){
        //     checkCompile(service_name, 0)
        // }
    }

    errorCallback = function(error) {
        $("#task_status_check_"+uuid).children().removeClass("spinner")
        $("#task_status_check_"+uuid).children().removeClass("loading")
        $("#task_status_check_"+uuid).children().addClass("close")
        $("#task_status_check_"+uuid).addClass("red")
        $("#task_status_check_"+uuid).removeClass("olive")
        $("#task_status_check_"+uuid).attr("show-code-key", file_path)
        $("#task_status_check_"+uuid).attr("show-code-value", error)
    }

    sendAjaxRequest('/step_code/merge_file', "POST", requestData, successCallback, errorCallback, true, false)
}

function referenceRepair(newCode, fileTask, uuid, referenceFile, repo, file_path) {
    console.log("referenceRepair:", newCode, fileTask, uuid)

    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_check_button tiny `+service_name.replace("/","-")+`" id="task_status_check_` + uuid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["self_check"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_button').popup();

    var requestData = JSON.stringify({ 'new_code': newCode, 'file_task': fileTask, 'reference_file': referenceFile, 'repo': repo, 'task_id': getTaskID(), 'file_path': file_path })

    successCallback = function(data) {
        $("#task_status_check_"+uuid).children().removeClass("spinner")
        $("#task_status_check_"+uuid).children().removeClass("loading")
        $("#task_status_check_"+uuid).children().addClass("check")
        $("#task_status_check_"+uuid).addClass("green")
        $("#task_status_check_"+uuid).removeClass("olive")
        $("#task_status_check_"+uuid).attr("show-code-key", file_path)
        $("#task_status_check_"+uuid).attr("show-code-value", escapeHtml(data.data["code"]))
        $("#task_status_check_"+uuid).attr("show-code-reason", escapeHtml(data.data["reasoning"]))

        gloablCode["newCode_" + uuid] = data.data["code"]

        // 暂时改为手动去点检查
        // if(globalTasks[service_name.replace("/","-")].length == $('.'+service_name.replace("/","-")+'.green.task_status_check_button').length){
        //     checkCompile(service_name, 0)
        // }
    }

    errorCallback = function(error){
        $("#task_status_check_"+uuid).children().removeClass("spinner")
        $("#task_status_check_"+uuid).children().removeClass("loading")
        $("#task_status_check_"+uuid).children().addClass("close")
        $("#task_status_check_"+uuid).addClass("red")
        $("#task_status_check_"+uuid).removeClass("olive")
        $("#task_status_check_"+uuid).attr("show-code-key", file_path)
        $("#task_status_check_"+uuid).attr("show-code-value", error)
    }

    sendAjaxRequest('/step_code/reference_repair', "POST", requestData, successCallback, errorCallback, true, false)
}

function editTaskDo(service_name, file_idx, uuid) {
    globalTasks[service_name.replace("/","-")][file_idx]["file-path"] = $("#task_file_path_" + uuid).val();
    globalTasks[service_name.replace("/","-")][file_idx]["code-edit-task"] = $("#task_file_contents_" + uuid).val();

    str = `
            <tr>
            <td class="two wide column">`+globalFrontendText["modify_file"]+`</td>
            <td>`+ $("#task_file_path_" + uuid).val() + `</td>
            </tr>
            <tr>
            <td>`+globalFrontendText["reasonfor_for_modification"]+`</td>
            <td>`+ globalTasks[service_name.replace("/","-")][file_idx]["code-interpreter"] + `</td>
            </tr>
            <tr>
            <td>`+globalFrontendText["adjust_code"]+`</td>
            <td>`+ $("#task_file_contents_" + uuid).val() + `</td>
            </tr>
            <tr>
            <td>`+globalFrontendText["status"]+`</td>
            <td id="task_status_td_`+ uuid + `">
                <button class="ui tiny grey button"><i class="stop circle outline icon"></i>已调整</button>
            </td>
            </tr>
            <tr>
            <td>`+globalFrontendText["operation"]+`</td>
            <td id="task_`+ uuid + `">
                <button class="ui tiny blue button" onClick="editTask('` + service_name + `',` + file_idx + `)"><i class="edit outline icon"></i>`+globalFrontendText["adjust_code"]+`</button>
                <button class="ui orange button tiny" onClick="editFileTask('` + service_name + `',` + file_idx + `)"><i class="play icon"></i>`+globalFrontendText["restart"]+`</button>
                <button class="ui brown button tiny"  onClick="compareCode('`+ uuid + `')"><i class="code icon"></i>`+globalFrontendText["review_code"]+`</button>
            </td>
            </tr>
    `
    $("#task_tbod_" + uuid).html(str)
    $("#task-model").modal('hide');
}

function editTask(service_name, file_idx) {
    var uuid = globalTasks[service_name.replace("/","-")][file_idx]["uuid"];
    var file_path = globalTasks[service_name.replace("/","-")][file_idx]["file-path"]
    var contents = globalTasks[service_name.replace("/","-")][file_idx]["code-interpreter"]

    var task_content = `
        <div class="ui form">
            <div class="field">
                <label>`+globalFrontendText["modify_file"]+`</label>
                <input type="text" value="`+ file_path + `" id="task_file_path_` + uuid + `">
            </div>
            <div class="field">
                <label>`+globalFrontendText["reasonfor_for_modification"]+`</label>
                <textarea rows="4" disabled>`+ contents + `</textarea>
            </div>
            <div class="field">
                <label>`+globalFrontendText["adjust_code"]+`</label>
                <input type="text" placeholder="" id="task_file_contents_` + uuid + `">
            </div>
            <button class="ui button green" type="submit" onClick="editTaskDo('`+ service_name + `',` + file_idx + `,'` + uuid + `')">`+globalFrontendText["submit"]+`</button>
        </div>
    `

    $("#task-content").html(task_content)
    $("#task-model").modal('show');
}

function getIdxByUUID(service_name, uuid) {
    var file_idx = 0
    globalTasks[service_name.replace("/","-")].forEach(function (file, file_index, element_array) {
        if (file.uuid == uuid) {
            file_idx = file_index
        }
    });
    return file_idx
}

function pluginTaskList(info, ifRecover) {
    console.log("----")
    console.log(info)

    $(".ai-prompt-area").hide()
    $('#err-message').html('<i class="recycle icon green big"></i><a href="/task.html?app_id='+globalAppInfo["app_id"]+'&branch='+globalAppInfo["default_target_branch"]+'&app_name='+globalAppInfo["app"]["name"]+'" target="_blank">'+globalFrontendText['task_code_finish']+"</a>")

    var service_name = info["service_name"]
    
    if (!ifRecover) {
        createWS(service_name)
    }

    var str = `<p>`+globalFrontendText["ai_api_subtask"]+`</p>`

    globalTasks[service_name.replace("/","-")] = info["files"]
    
    var service_str = `
        <h4 class="ui horizontal divider header">
            <i class="coffee icon brown"></i>
            `+ service_name + `
        </h4>
        <div class="ui yellow visible message">`+globalFrontendText["operation"]+`: 
            <button class="ui green button tiny" onclick="checkCompile('`+ service_name +`', 0);"><i class="tasks icon"></i>`+globalFrontendText["auto_check"]+`</button>
            >>
            <button class="ui blue button tiny" onclick="resetWorkspace('`+ service_name +`', this);"><i class="sync icon"></i>`+globalFrontendText["reset_workspace"]+`</button>
            <button class="ui blue button tiny" onclick="startPush('`+ service_name +`', this);"><i class="tasks icon"></i>`+globalFrontendText["submit_code"]+`</button>
            >>
            <button class="ui teal button tiny" onClick="startCi('`+ service_name + `', this)"><i class="tasks icon"></i>`+globalFrontendText["start_ci"]+`</button>
            >>
            <button class="ui purple button tiny" onClick="startCd('`+ service_name + `')"><i class="docker icon"></i>`+globalFrontendText["start_cd"]+`</button>
        </div>
    `;

    info["files"].forEach(function (file, file_index, file_array) {
        var uuid = Math.random().toString(36).substr(2, 9) + Date.now().toString();
        globalTasks[service_name.replace("/","-")][file_index].uuid = uuid
        gloablCode["newCode_" + uuid] = file["code"]
        gloablCode["oldCode_" + uuid] = file["old-code"]
        service_str = service_str + `
            <table class="ui definition table">
            <tbody id="task_tbod_`+ uuid + `">
                <tr>
                <td class="two wide column">`+globalFrontendText["modify_file"]+`</td>
                <td>`+ file["file-path"] + `</td>
                </tr>
                <tr>
                <td>`+globalFrontendText["reasonfor_for_modification"]+`</td>
                <td>`+ file["code-interpreter"].replaceAll('\n', '<br />') + `</td>
                </tr>
                <tr>
                <td>`+globalFrontendText["status"]+`</td>
                <td id="task_status_td_`+ uuid + `">
                    <button class="ui circular check green icon button task_status_button tiny" id="task_status_` + uuid + `" data-content="" onClick="showCode(this)" show-code-key="`+file["file-path"]+`" show-code-reason=""><i class="check icon"></i> `+globalFrontendText["initial_code"]+`</button>
                </td>
                </tr>
                <tr>
                <td>`+globalFrontendText["operation"]+`</td>
                <td id="task_`+ uuid + `">
                    <button class="ui tiny blue button" onClick="editTask('` + service_name + `',` + file_index + `)"><i class="edit outline icon"></i>`+globalFrontendText["adjust_code"]+`</button>
                    <button class="ui orange button tiny" onClick="editFileTask('` + service_name + `',` + file_index + `)"><i class="play icon"></i>`+globalFrontendText["restart"]+`</button>
                    <button class="ui brown button tiny"  onClick="compareCode('`+ uuid + `')"><i class="code icon"></i>`+globalFrontendText["review_code"]+`</button>
                </td>
                </tr>
            </tbody>
            </table>
        `
    });
    str += service_str;

    var ai_code_class = service_name.replace("/","-")
    if ($('.ai-code.'+ai_code_class).length > 0) {
        $(".ai-code."+ai_code_class).eq($('.ai-code.'+ai_code_class).length - 1).html(str);
    } else {
        $(".ai-code").eq($('.ai-code').length - 1).html(str);
    }
    
    info["files"].forEach(function (file, file_index, file_array) {
        var uuid = file.uuid;
        $("#task_status_"+uuid).attr("show-code-value", escapeHtml(gloablCode["newCode_" + uuid]));
    });

    $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    $('.plugin-task-list-play').popup();
    $('.task_status_button').popup();

    if (!ifRecover) {
        setTimeout(function () {
            info["files"].forEach(function (file, file_index, file_array) {
                if (file.hasOwnProperty("step") && file["step"].length > 0) {
                    checkCode(file["code"], file["code-interpreter"], file["uuid"], file["file-path"], info["service_name"], file["step"])
                } else if (file["old-code"].length > 0) {
                    mergeCode(file["uuid"], file["code"], file["old-code"], file["code-interpreter"], info["service_name"], file["file-path"])
                } else if (file["code"].length > 0 && typeof file["reference-code"] !== "undefined" && file["reference-code"].length > 0) {
                    referenceRepair(file["code"], file["code-interpreter"], file["uuid"], file["reference-file"], info["service_name"], file["file-path"])
                } else {
                    checkCode(file["code"], file["code-interpreter"], file["uuid"], file["file-path"], info["service_name"])
                }
            })
        }, 1000);
    }
}

function resetWorkspace(serviceName, ele) {
    $(ele).addClass("loading")
    $(ele).addClass("disabled")
    
    var requestData = JSON.stringify({ 'service_name': serviceName, 'task_id': getTaskID() })

    successCallback = function(data){
        $(ele).removeClass("loading")
        $(ele).removeClass("disabled")
    }

    ErrorCallback = function(error) {
        $(ele).removeClass("loading")
        $(ele).removeClass("disabled")

        if (typeof error === 'undefined') {
            error = "Unknown error"
        }
        myAlert("ERROR", error)
    }

    sendAjaxRequest('/workspace/resetWorkspace', "POST", requestData, successCallback, ErrorCallback, false, false)
}

function startPush(serviceName, ele, hideMessage) {
    $(ele).addClass("loading")
    $(ele).addClass("disabled")

    setTimeout(function() {
        resetWorkspace(serviceName, ele)

        // save all code
        globalTasks[serviceName].forEach(function (file, element_index, element_array) {
            let uuid = file.uuid
            let file_path = file["file-path"]
            saveCode(serviceName, file_path, uuid)
        })

        $(ele).addClass("loading")
        $(ele).addClass("disabled")

        var requestData = JSON.stringify({ 'service_name': serviceName, 'task_id': getTaskID() })

        successCallback = function(data){
            $(ele).removeClass("loading")
            $(ele).removeClass("disabled")

            if (!hideMessage) {
                myAlert(globalFrontendText["ok"], data.data)
            }
        }

        ErrorCallback = function(error) {
            $(ele).removeClass("loading")
            $(ele).removeClass("disabled")

            if (typeof error === 'undefined') {
                error = "Unknown error"
            }

            var retruBtn = '<br /><br /><button class="ui green button" onClick="createWS(\''+serviceName+'\')">'+globalFrontendText["repair_workspace"]+'</button>'
            myAlertPure("ERROR", error + retruBtn)
        }

        sendAjaxRequest('/workspace/gitpush', "POST", requestData, successCallback, ErrorCallback, true, false)
    }, 100);
}

function startCi(repo_path, ele) {  
    startPush(repo_path, ele, true);

    customPrompt = "git repo: "+repo_path+" "+globalFrontendText["start_ci"]

    thinkUI(customPrompt, globalFrontendText["ai_think"], "QA")
    
    var requestData = JSON.stringify({ 'repo_path': repo_path, 'task_id': getTaskID()})

    successCallback = function(data) {
        pluginci(data.data.info)
    }

    sendAjaxRequest('/step_devops/trigger_ci', "POST", requestData, successCallback, aiErrorCallback, true, true)
}

startCDsuccessCallback = function(data) {
    var str = globalFrontendText["start_cd"]+": "+data.data["internet_ip"]
    $(".ai-code").eq($('ai-code').length - 1).html(str);
}

function startCd(repo_path) {  
    customPrompt = globalFrontendText["start_cd"]+": "+repo_path

    thinkUI(customPrompt, globalFrontendText["ai_think"], "OP")
    
    var requestData = JSON.stringify({ 'repo_path': repo_path, 'task_id': getTaskID(), 'docker_image': globalDockerImage})

    sendAjaxRequest('/step_devops/trigger_cd', "POST", requestData, startCDsuccessCallback, aiErrorCallback, true, true)
}

function useGoodCase(classname) {
    prompt = $("."+classname).text()
    $('#prompt-textarea').val(prompt)
    $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
}

function taskOk(newPrompt, element, operType) {
    var prompt = decodeURI(newPrompt)
    $(element).addClass("disabled");
    $('#prompt-hidePrompt').val(operType);

    $('#prompt-textarea').val(prompt)
    $('#generate-code-button').click()
}

function taskChange(newPrompt, operType, serviceName) {
    var prompt = decodeURI(newPrompt)
    
    $('#generate-code-button').removeClass("disabled");
    $(".ai-prompt-container").last().children().children().find("textarea").val(prompt);
    globalContext = []
    $('#prompt-hidePrompt').val(operType);
    $("#prompt-serviceName").val(serviceName)
    $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
}

function pluginci(info, uuid) {
    if (info["piplineID"]) {
        refreshPluginciStatus(info["piplineID"], info["repopath"], info["piplineUrl"], undefined, 1, uuid)
    }
}

function refreshPluginciStatus(piplineID, repopath, piplineUrl, element, times, uuid) {
    if (typeof times === 'number' && times % 1 === 0) {
        times++
    } else {
        var times=0
    }
    $(element).addClass('loading');
    info = { "piplineID": piplineID, "repopath": repopath, 'task_id': getTaskID() }
    $.ajax({
        type: 'GET',
        xhrFields: {
            withCredentials: true
        },
        url: apiUrl + '/step_devops/query_ci',
        data: info,
        contentType: 'application/json',
        dataType: 'json'
    }).done(data => {
        if( data.success ) {
            data=data.data
            console.log(data)
            globalDockerImage = data.docker_mage
            var loadingClass = ""
            if( times < 20 ) {
                loadingClass = "loading"
            }
            var str = `<h4>`+globalFrontendText["start_ci"]+` <div class="ui olive `+loadingClass+` button" onclick="refreshPluginciStatus('` + piplineID + `','` + repopath + `', '`+piplineUrl+`', this, 20)"><i class="sync icon"></i>`+globalFrontendText["update_status"]+`</div><div class="ui blue button" onclick="window.open('`+piplineUrl+`', '_blank');"><i class="tasks icon"></i>`+globalFrontendText["view_detail"]+`</div></h4><div class="ui middle aligned divided list">`
            var allDone = true
            data["piplineJobs"].forEach(element => {
                var jobDone = false
                let icon = '<i class="pause circle brown icon big pluginci-status" data-title='+element['status']+'></i>'
                if (element['status'] == 'success') {
                    jobDone = true
                    icon = '<i class="check circle green icon big pluginci-status" data-title='+element['status']+'></i>'
                } else if (element['status'] == 'failed' || element['status'] == 'canceled') {
                    icon = '<i class="times circle red  icon big pluginci-status" data-title='+element['status']+'></i>'
                    jobDone = true
                }
                str += '<div class="item"><div class="right floated content"><div data-title="执行日志" onClick="myAlert(\'任务日志\',\''+element['log']+'\')" class="ui button pluginci-status">查看日志</div></div>'+icon+'<div class="content">' + element['job_name'] + '</content></div></div>'
                if (jobDone==false) {
                    allDone = false    
                }
            });
            if (allDone) {
                str = str.replace("ui olive loading button", "ui olive button")
                times = 20
            }
            str += '</div>'

            
            if (uuid && uuid.length > 0 ) {
                $("."+uuid).html(str);
            } else {
                $(".ai-code").eq($('ai-code').length - 1).html(str);
            }

            // $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
            $('.pluginci-refresh').popup();
            $('.pluginci-status').popup();
            setTimeout(function () {
                if( times < 20 ) {
                    refreshPluginciStatus(piplineID, repopath, piplineUrl, element, times)
                }
            }, 20000);
        } else {
            myAlert(globalFrontendText["error"], data.error)
        }
    }).fail(function () {

    });
}

function convertURLsToLinks(str) {
  var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;

  var replacedText = str.replace(urlRegex, function(url) {
    var fullURL = url;
    if (!fullURL.match('^https?:\/\/')) {
      fullURL = 'http://' + fullURL;
    }
    return '<a href="' + fullURL + '" target="_blank">' + url + '</a>';
  });

  return replacedText;
}

function clarifyOk(element) {
    $(element).addClass("disabled");
    var previousTable = $(element).prev('table'); 
    var inputs = previousTable.find('input'); 
    var content = ""
    var question = 1
    inputs.each(function() { 
        $(this).prop('disabled', true);
        let q = $(this).parent().parent().prev().children("span").text()
        content += globalFrontendText["question"]+question+", "+q+" 回答："+$(this).val()+"；\n"; 
        question++
    }); 
    clarify(content)
}

clarifySuccessCallback = function(data, isRecover){
    $('#generate-code-button').removeClass("disabled");

    data = data.data
    var msgJson = data.message
    var msgStr = JSON.stringify(msgJson)
    var msg = ""
    var str = ""
    globalContext.push({ role: 'user', content: data.input_prompt })
    globalContext.push({ role: 'assistant', content: msgStr })    
    if (msgStr.includes("development_requirements_overview")) {
        if (msgJson["services_involved"].length > 0) {
            globalChangeServiceList = []
            msgJson["services_involved"].forEach(function (element, element_index, element_array) {
                globalChangeServiceList.push(element["service_name"])
            })
        }
        if (globalChangeServiceList < 0 ) {
            myAlert(globalFrontendText["error"], globalFrontendText["service_modification_item_empty"])
        }
        msg = msgJson.development_requirements_detail
        str = '<br /><br /><button class="ui green button" onClick="taskOk(\''+escapeHtml(msg)+'\', this, \'requirement_doc\')">'+globalFrontendText["submit"]+'</button><button class="ui blue button" onclick="taskChange(\''+escapeHtml(msg)+'\', \'requirement_doc\')">'+globalFrontendText["edit"]+'</button>'
        marked_msg = marked.marked(msg)
        marked_msg = marked_msg.replaceAll("</code></pre>", "")
        marked_msg = marked_msg.replaceAll("<pre><code>", "")
        console.log(marked_msg)
        msg = '<h5>'+globalFrontendText["ai_requirement_clarify_3"]+'</h5>'+marked_msg
    } else {
        var table = '<h5>'+globalFrontendText["ai_requirement_clarify_4"]+'</h5><table class="ui celled table"><thead><tr><th class="eight wide">'+globalFrontendText["question"]+'</th><th class="eight wide">'+globalFrontendText["answer"]+'</th></tr></thead><tbody>'
        console.log(msgJson)
        msgJson.forEach(function (element, element_index, element_array) {
            table += '<tr><td><span>'+element["question"]+"</span>"+element["reasoning"]+'</td><td><div class="ui fluid icon input"><input type="text" name="clarify_answer" value="'+element["answer_sample"]+'" placeholder="'+globalFrontendText["answer"]+'" autocomplete="off"></div></td></tr>'
        })
        table += '</tbody></table><button class="ui green button" onclick="clarifyOk(this)">'+globalFrontendText["submit"]+'</button>'
        msg = table
    }

    $(".ai-code").eq($('ai-code').length - 1).html(msg+str);

    if (!isRecover && msgStr.includes("review") && msgJson["review"].length>10){
        $("#prompt-textarea").val(msgJson["review"].replaceAll('\n\n', '\n'))
        globalRole = "TL"
        $("#generate-code-button").click()
    } 
    //$(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
}

function clarify(customPrompt, thisElement) {
    customPrompt = decodeURI(customPrompt)
    $(thisElement).addClass("disabled");

    thinkUI(customPrompt, globalFrontendText["ai_think"], 'PM')

    var requestData = JSON.stringify({ 'user_prompt': customPrompt, 'global_context': JSON.stringify(globalContext), 'task_id': getTaskID() })
    var retruBtn = '<br /><br /><button class="ui green button" onClick="clarify(\''+escapeHtml(customPrompt)+'\', this)">重试</button>'

    errorCallback = function(errorMsg) {
        $(".ai-code").eq($('ai-code').length - 1).html(errorMsg+retruBtn);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    }

    sendAjaxRequest('/step_requirement/clarify', "POST", requestData, clarifySuccessCallback, errorCallback, true, true)
}

genInterfaceDocSuccessCallback = function(data) {
    data = data.data
    var msg = data.message
    str = "<pre>"+msg+"</pre>"
    str += '<br /><button class="ui green button" onClick="taskOk(\''+escapeHtml(msg)+'\', this, \'api_doc\')">'+globalFrontendText["submit"]+'</button><button class="ui blue button" onclick="taskChange(\''+escapeHtml(msg)+'\', \'api_doc\')">'+globalFrontendText["edit"]+'</button>'

    str = '<h5>'+globalFrontendText["ai_api_clarify_1"]+'</h5><br />'+str
    $(".ai-code").eq($('ai-code').length - 1).html(str);
    $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
}

function genInterfaceDoc(customPrompt, thisElement) {
    customPrompt = decodeURI(customPrompt)
    $(thisElement).addClass("disabled");

    thinkUI(customPrompt, globalFrontendText["ai_think"], 'TL')

    var requestData = JSON.stringify({ 'user_prompt': customPrompt, 'task_id': getTaskID() })
    var retruBtn = '<br /><br /><button class="ui green button" onClick="genInterfaceDoc(\''+escapeHtml(customPrompt)+'\', this)">'+globalFrontendText["retry"]+'</button>'

    errorCallback = function(errorMsg) {
        $(".ai-code").eq($('ai-code').length - 1).html(errorMsg+retruBtn);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    }

    sendAjaxRequest('/step_api/clarify', "POST", requestData, genInterfaceDocSuccessCallback, errorCallback, true, true)
}

taskAnalysisSuccessCallback = function(data, isRecover){
    $('#generate-code-button').removeClass("disabled");

    data = data.data
    var msg = data.message
    var service_name = data.service_name
    var ai_code_class = service_name.replace("/","-")
    var str = ""  
    str = '<br /><br /><button class="ui green button" onClick="taskSplitOK(\''+escapeHtml(msg)+'\', \''+service_name+'\', this)">'+globalFrontendText["submit"]+'</button><button class="ui blue button" onclick="taskChange(\''+escapeHtml(msg)+'\', \'tec_doc\', \''+service_name+'\')">'+globalFrontendText["edit"]+'</button>'
    marked_msg = marked.marked(msg)
    msg = '<h5>'+globalFrontendText["ai_tecDoc_clarify_1"]+'</h5>'+marked_msg

    $("."+ai_code_class).eq($(ai_code_class).length - 1).html(msg+str);
}

function taskAnalysis(customPrompt, service_name, hideUserPrompt, thisElement) {
    customPrompt = decodeURI(customPrompt)
    $(thisElement).addClass("disabled");

    $('#prompt-textarea').val("");
    $("#prompt-hidePrompt").val("")
    var ai_code_class = service_name.replace("/","-")
    var newField = $('<div class="user-code-container"><div class="ui container grid"><div class="one wide column"><i class="blue  grav icon big" style="font-size: 3em;"></i></div><div class="fifteen wide column ai-content"><div class="ai-code" id="">'+globalFrontendText["ai_api_clarify_confirm"]+'</div></div></div></div> <div class="ai-code-container '+ai_code_class+'"><div class="ui container grid"><div class="one wide column"><img class="ui avatar image" src="./static/image/role_tl.jpeg" data-content="TL" style="width: auto;height: auto;"></div><div class="fifteen wide column ai-content"><div class="ai-code '+ai_code_class+'"><i class="spinner loading icon"></i>'+globalFrontendText["ai_api_subtask_1"]+' '+service_name+' '+globalFrontendText["ai_api_subtask_2"]+'</div></div></div></div>');
    $(".ai-prompt-container").before(newField);
    $(".ai-code-container."+ai_code_class).eq($('.ai-code-container.'+ai_code_class).length - 1).hide();
    $(".user-code-container").eq($('.user-code-container').length - 1).hide();
    if (!hideUserPrompt) {
        setTimeout(function () {
            $(".user-code-container").eq($('.user-code-container').length - 1).slideDown();
        }, 200);
    }
    setTimeout(function () {
        $(".ai-code-container."+ai_code_class).eq($('ai-code-container.'+ai_code_class).length - 1).slideDown();
    }, 700);
    // 滚动到页面底部
    setTimeout(function () {
        $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
    }, 900);
    $('img').popup();

    doc_type = "api"
    if (globalChangeServiceList.length == 1) {
        doc_type = "prd"
    }
    var requestData = JSON.stringify({ 'service_name': service_name, 'prompt': customPrompt, 'doc_type': doc_type, 'task_id': getTaskID() })

    var retruBtn = '<br /><br /><button class="ui green button" onClick="taskAnalysis(\''+escapeHtml(customPrompt)+'\',\''+service_name+'\', true, this)">'+globalFrontendText["retry"]+'</button>'

    errorCallback = function(errorMsg) {
        $(".ai-code."+ai_code_class).eq($('.ai-code.'+ai_code_class).length - 1).html(service_name+errorMsg+retruBtn);
    }

    sendAjaxRequest('/step_subtask/analysis', "POST", requestData, taskAnalysisSuccessCallback, errorCallback, true, true)
}

function taskSplitOK(customPrompt, service_name, thisElement) {
    customPrompt = decodeURI(customPrompt)
    $(thisElement).addClass("disabled");

    var msg = customPrompt
    if (thisElement) {
        msg = globalFrontendText["ai_api_clarify_confirm"]
    }

    $('#prompt-textarea').val("");
    $("#prompt-hidePrompt").val("")
    $("#prompt-serviceName").val("")
    var ai_code_class = service_name.replace("/","-")
    var newField = $('<div class="user-code-container"><div class="ui container grid"><div class="one wide column"><i class="blue  grav icon big" style="font-size: 3em;"></i></div><div class="fifteen wide column ai-content"><div class="ai-code" id="">'+msg+'</div></div></div></div> <div class="ai-code-container '+ai_code_class+'"><div class="ui container grid"><div class="one wide column"><img class="ui avatar image" src="./static/image/role_tl.jpeg" data-content="TL" style="width: auto;height: auto;"></div><div class="fifteen wide column ai-content"><div class="ai-code '+ai_code_class+'"><i class="spinner loading icon"></i>'+globalFrontendText["ai_api_subtask_1"]+' '+service_name+' '+globalFrontendText["ai_api_subtask_2"]+'</div></div></div></div>');
    $(".ai-prompt-container").before(newField);
    $(".ai-code-container."+ai_code_class).eq($('.ai-code-container.'+ai_code_class).length - 1).hide();
    $(".user-code-container").eq($('.user-code-container').length - 1).hide();
    setTimeout(function () {
        $(".user-code-container").eq($('.user-code-container').length - 1).slideDown();
    }, 200);
    setTimeout(function () {
        $(".ai-code-container."+ai_code_class).eq($('ai-code-container.'+ai_code_class).length - 1).slideDown();
    }, 700);
    // 滚动到页面底部
    setTimeout(function () {
        $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
    }, 900);
    $('img').popup();

    doc_type = "api"
    if (globalChangeServiceList.length == 1) {
        doc_type = "prd"
    }
    var requestData = JSON.stringify({ 'service_name': service_name, 'prompt': customPrompt, 'doc_type': doc_type, 'task_id': getTaskID() })

    var retruBtn = '<br /><br /><button class="ui green button" onClick="taskSplitOK(\''+escapeHtml(customPrompt)+'\',\''+service_name+'\', this)">'+globalFrontendText["retry"]+'</button>'

    successCallback = function(data) {
        data = data.data
        var plugin = data.plugin
        if (plugin) {
            triggerPlugin(plugin)
        }
    }

    errorCallback = function(errorMsg) {
        $(".ai-code."+ai_code_class).eq($('.ai-code.'+ai_code_class).length - 1).html(service_name+errorMsg+retruBtn);
    }

    sendAjaxRequest('/step_subtask/task_split', "POST", requestData, successCallback, errorCallback, true, true)
}

function escapeHtml(html) {
  return encodeURI(html.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/g, ' '));
}

function decodeHTML(encodedHTML) {
    // 首先将编码后的字符串中的空格还原为单引号
    var decodedHTML = encodedHTML.replace(/ /g, "'");
    
    // 然后将编码后的特殊字符还原为原始的字符
    decodedHTML = decodeURIComponent(decodedHTML);
  
    // 最后将 '&lt;' 替换回 '<'，将 '&gt;' 替换回 '>'
    decodedHTML = decodedHTML.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    
    return decodedHTML;
  }

function compareCode(uuid) {
    console.log(uuid)
    var code = decodeURI(escapeHtml(gloablCode["newCode_" + uuid]));
    var oldcode = decodeURI(escapeHtml(gloablCode["oldCode_" + uuid]));
    $('#diff-output').html('<pre >Compare...</pre>');
    $("#code-actions-uuid").val(uuid)
    $('#model-diff').modal('show');

    var diff = Diff.createTwoFilesPatch('Old', 'New', oldcode, code);

    var result = '';
    var lines = diff.split('\n');

    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];

        if (line.startsWith('-')) {
            result += '<span style="background-color: red;">' + line + '</span><br>';
        } else if (line.startsWith('+')) {
            result += '<span style="background-color: green;">' + line + '</span><br>';
        } else {
            result += line + '<br>';
        }
    }
    $('#diff-output').html('<pre >' + result + '</pre>');
    $('#model-diff').modal('hide').modal('show');
};


function hideMiddleCharacters(inputString, mid) {
    if (inputString == null) {
        return "****"
    }
    const middleIndex = Math.floor(inputString.length / mid);
    const firstHalf = inputString.slice(0, middleIndex);

    const hiddenMiddle = '*'.repeat(middleIndex);
    return firstHalf + hiddenMiddle ;
}

function getTaskID() {
    var queryString = window.location.search;

    var params = new URLSearchParams(queryString);

    var taskId = params.get('task_id');

    return taskId
}

function getUrlParams(pkey) {
    var queryString = window.location.search;

    var params = new URLSearchParams(queryString);

    var taskId = params.get(pkey);

    return taskId
}

function getTenantID() {
    var queryString = window.location.search;
    var params = new URLSearchParams(queryString);
    var tenant_id = params.get('tenant_id');
    if (!tenant_id) {
        tenant_id = globalTenantID
    }
    return tenant_id
}

function showUrlErrorMsg() {
    var queryString = window.location.search;
    var params = new URLSearchParams(queryString);
    var err = params.get('err');
    if (err && err.length>0) {
        myAlert(globalFrontendText["error"], err)
    }
}
