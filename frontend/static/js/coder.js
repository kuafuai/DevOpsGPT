var globalContext = []
var globalMemory = {}
var globalTasks = []
var gloablCode = {}
var globalFrontendText = {}
var globalCompileTimes = {}
var globalChangeServiceList = []
var codeMirror
var apiUrl = "http://127.0.0.1:8081"

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
                errorCallback(data.error + "<br />" + globalFrontendText["backend_return_error"]);
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


function thinkUI(customPrompt, thinkText) {
    $('#prompt-textarea').val("");
    $("#prompt-hidePrompt").val("")
    var newField = $('<div class="user-code-container"><div class="ui container grid"><div class="one wide column"><i class="blue  odnoklassniki square icon big" style="font-size: 3em;"></i></div><div class="fifteen wide column ai-content"><div class="ai-code">' + customPrompt.replaceAll("\n", "<br />") + '</div></div></div></div> <div class="ai-code-container"><div class="ui container grid"><div class="one wide column"><i class="orange reddit square icon big" style="font-size: 3em;"></i></div><div class="fifteen wide column ai-content"><div class="ai-code"><i class="spinner loading icon"></i>'+thinkText+'</div></div></div></div>');
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

function modelInfoRead(appName, appCode) {
    requestData = JSON.stringify({ "app_name": appName })

    successCallback = function(data) {
        $("#mode-edit-content").val(data.content)
        $("#mode-edit-app-name").val(appName)
    }

    sendAjaxRequest('/app/get', 'POST', requestData, successCallback, alertErrorCallback, true, false)
}

function modelSelected(appName, appID, repos) {
    source_branch = $("#model_source_branch_" + appID).val()
    feature_branch = $("#model_feature_branch_" + appID).val()
    customPrompt = globalFrontendText["ai_select_app"] + ": " + appName
    $('.model-selector').addClass("disabled")
    $("#generate-code-button").removeClass("disabled")
    $('#model-modal').modal('hide');

    thinkUI(customPrompt, globalFrontendText["ai_think"])

    requestData = JSON.stringify({ "app_id": appID, "source_branch": source_branch, "feature_branch": feature_branch })

    successCallback = function(data){
        data = data.data
        globalChangeServiceList = data.repo_list
        str = globalFrontendText["ai_selected_app_1"] + ": " + appName
            +"<br />"+ globalFrontendText["ai_selected_app_2"] + ": "+ data["task_id"]
            +"<br />"+ globalFrontendText["ai_selected_app_3"] + ": "+ repos
            +"<br />"+ globalFrontendText["ai_selected_app_4"] + source_branch +" "+ globalFrontendText["ai_selected_app_5"] +" "+ feature_branch
            +"<br /><br />" + globalFrontendText["ai_selected_app_6"];
        const url = window.location;
        const newUrl = url.origin + '?task_id=' + data.task_id;
        history.pushState('', '', newUrl); 
        answerUI(str)
    }

    errorCallback = function (error){
        $('.model-selector').removeClass("disabled")
        str = error
        $(".ai-code").eq($('ai-code').length - 1).html(str);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
        setTimeout(function () {
            $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
        }, 1000);
    }

    sendAjaxRequest('/task/setup_app', 'POST', requestData, successCallback, errorCallback, true, true)
}

$(document).ready(function () {
    language()
    logincheck()

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

                str += `
                    <div class="item" style="padding: 15px 0px;">
                        <div class="content">
                        <div class="header" style="line-height: 25px;">
                            `+globalFrontendText["app"]+`: `+app.name+`
                            <br />
                            `+globalFrontendText["ai_selected_app_4"]+`
                            <input type="text" placeholder="" value="`+app.default_source_branch+`" class="fenzhiguifan" id="model_source_branch_`+app.id+`">
                            `+globalFrontendText["ai_selected_app_5"]+`
                            <input type="text" placeholder="" value="`+app.default_target_branch+`" class="fenzhiguifan" id="model_feature_branch_`+app.id+`">
                        </div>
                        <div class="description" style="line-height: 25px;">`+app.intro+`</div>
                        <!-- div class="ui button green model-selected" onClick="modelInfoRead('`+app.name+`','`+app.id+`', '`+escapeHtml(app.intro)+`', '`+app.api_doc_url+`', '`+app.repos+`')" style="float: right;"></div -->
                        <div class="ui button blue model-selected" onClick="modelSelected('`+app.name+`','`+app.id+`', '`+repos+`')" style="float: right;">`+globalFrontendText["start"]+`</div> 
                        </div>
                    </div>
                `
            })
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
        if (operType == "api_doc") {
            globalChangeServiceList.forEach(function (element, element_index, element_array) {
                if (element_index > 0 ) {
                    setTimeout(function () {
                        taskAnalysis(customPrompt, element, true)
                    }, 200);
                } else {
                    taskAnalysis(customPrompt, element)
                }
            })
        }else if (operType == "requirement_doc") {
            genInterfaceDoc(customPrompt)
        } else {
            clarify(customPrompt)
        }
    });

    $('#cancel-task').click(function () {
        location.reload();
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
              $(".f_"+key).text(value)
            }
        }
    }

    errorCallback = function(data) {
        console.log(data)
        $("#my-login").modal('show')
        myAlertPure("Error 错误", "The back-end service interface cannot be accessed. Please check the terminal service log and browser console. (Usually the back-end service is not started, Or exists <a href='https://github.com/kuafuai/DevOpsGPT/blob/master/docs/DOCUMENT.md#configuration-details' target='_blank'> Cross-domain problem? </a>)<br /><br />无法访问后端服务接口，请检查终端服务日志以及浏览器控制台报错信息。（通常是后端服务没有启动，或存在 <a href='https://github.com/kuafuai/DevOpsGPT/blob/master/docs/DOCUMENT_CN.md#%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E7%B1%BB' target='_blank'>跨域问题？</a>）")
    }

    sendAjaxRequest('/user/language', 'GET', "", successCallback, errorCallback, true, false)
}

function logincheck() {
    successCallback = function(data) {
        var username = data.data.username
        const url = window.location;
        const newUrl = url.origin;
        history.pushState('', '', newUrl); 
        $("#current-username").html(username)
        $("#watermark-username").html(username)
    }

    errorCallback = function(data) {
        $("#my-login").modal('show')
    }

    sendAjaxRequest('/task/clear_up', 'GET', "", successCallback, errorCallback, true, false)
}

function logout() {
    successCallback = function() {
        location.reload();
    }

    sendAjaxRequest('/user/logout', "POST", "", successCallback, alertErrorCallback, true, true)
}

function changeLanguage() {
    successCallback = function() {
        location.reload();
    }

    sendAjaxRequest('/user/change_language', "GET", "", successCallback, alertErrorCallback, true, false)
}

function login() {
    var requestData = JSON.stringify({ 'username': $("#login-username").val(), 'password': $("#login-password").val() })
 
    successCallback = function(data) {
        location.reload();
    }

    errorCallback = function(error) {
        $("#login-message").html(error)
        $("#login-message").fadeOut().fadeIn()
    }

    sendAjaxRequest('/user/login', "POST", requestData, successCallback, errorCallback, true, false)
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
        pluginTaskList(plugin["info"])
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

function createWS(serviceName, sourceBranch, featureBranch) {
    var requestData = JSON.stringify({ 'repo_path': serviceName, 'base_branch': sourceBranch, 'feature_branch': featureBranch })

    successCallback = function(data){}

    errorCallback = function(error) {
        var retruBtn = '<br /><br /><button class="ui green button" onClick="createWS(\''+serviceName+'\', \''+sourceBranch+'\', \''+featureBranch+'\')">'+globalFrontendText["retry"]+'</button>'
        myAlertPure("ERROR", error + retruBtn)
    }

    sendAjaxRequest('/workspace/create', "POST", requestData, successCallback, errorCallback, false, false)
}

function fixLint(solution, uuid, file_path, service_name, times) {
    if (times >= 2) {
        return
    }
    var code = gloablCode["newCode_" + uuid]

    let buttonid = "task_status_fix_lint_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_fix_lint_button tiny `+service_name.replace("/","-")+`" id="` + buttonid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["fix_static_scan"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_fix_lint_button').popup();

    var requestData = JSON.stringify({ 'code': code, 'solution': solution })

    successCallback = function(data) {
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

function fixCompile(solution, uuid, file_path, service_name, times) {
    if (times >= 2) {
        return
    }
    var code = gloablCode["newCode_" + uuid]

    let buttonid = "task_status_fix_compile_"+globalCompileTimes[service_name.replace("/","-")]+"_"+times+"_"+uuid
    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_fix_compile_button tiny `+service_name.replace("/","-")+`" id="` + buttonid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["fix_compile_check"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_fix_compile_button').popup();

    var requestData = JSON.stringify({ 'code': code, 'solution': solution })
    
    successCallback = function(data) {
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
    var requestData = JSON.stringify({ 'service_name': service_name, 'file_path': filePath, "code": code})

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

    var requestData = JSON.stringify({ 'service_name': service_name, 'file_path': filePath })

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
            fixLint(data.data["reasoning"][0]["solution-analysis"], uuid, filePath, service_name, times)
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

function checkCode(code, fileTask, uuid, file_path, service_name) {
    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_check_button tiny `+service_name.replace("/","-")+`" id="task_status_check_` + uuid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["self_check"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_button').popup();

    var requestData = JSON.stringify({ 'code': code, 'fileTask': fileTask })

    successCallback = function(data){
        $("#task_status_check_"+uuid).children().removeClass("spinner")
        $("#task_status_check_"+uuid).children().removeClass("loading")
        $("#task_status_check_"+uuid).children().addClass("check")
        $("#task_status_check_"+uuid).addClass("green")
        $("#task_status_check_"+uuid).removeClass("olive")
        $("#task_status_check_"+uuid).attr("show-code-key", file_path)
        $("#task_status_check_"+uuid).attr("show-code-value", escapeHtml(data.data["code"]))
        $("#task_status_check_"+uuid).attr("show-code-reason", escapeHtml(data.data["reasoning"]))

        gloablCode["newCode_" + uuid] = data.data["code"]

        if(globalTasks[service_name.replace("/","-")].length == $('.'+service_name.replace("/","-")+'.green.task_status_check_button').length){
            checkCompile(service_name, 0)
        }
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

    sendAjaxRequest('/step_code/check_file', "POST", requestData, successCallback, errorCallback, true, false)
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

    var requestData = JSON.stringify({ 'repo_path': repo_path })

    successCallback = function(data) {
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
                        fixCompile(solution, uuid, file_path, repo_path, times)
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

    str = $("#task_status_td_" + uuid).html()+`
        <button class="ui circular olive icon button task_status_button tiny" id="task_status_redo_` + uuid + `" data-content="" onClick="showCode(this)"><i class="spinner loading icon"></i> `+globalFrontendText["initial_code"]+`</button>
        `
    $("#task_status_td_" + uuid).html(str)
    $('.task_status_button').popup();

    var requestData = JSON.stringify({ 'file_task': fileTask, 'new_task': newTask, 'new_code': newCode })

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

    var requestData = JSON.stringify({ 'file_task': fileTask, 'new_code': newCode, 'old_code': oldCode })

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

        if(globalTasks[service_name.replace("/","-")].length == $('.'+service_name.replace("/","-")+'.green.task_status_check_button').length){
            checkCompile(service_name, 0)
        }
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

    var requestData = JSON.stringify({ 'new_code': newCode, 'file_task': fileTask, 'reference_file': referenceFile, 'repo': repo })

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

        if(globalTasks[service_name.replace("/","-")].length == $('.'+service_name.replace("/","-")+'.green.task_status_check_button').length){
            checkCompile(service_name, 0)
        }
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

function pluginTaskList(info) {
    var service_name = info["service_name"]
    
    createWS(service_name, globalMemory["task_info"]["source_branch"], globalMemory["task_info"]["feature_branch"])

    var str = `<p>`+globalFrontendText["ai_api_subtask"]+`</p>`

    globalTasks[service_name.replace("/","-")] = info["files"]
    
    var service_str = `
        <h4 class="ui horizontal divider header">
            <i class="coffee icon brown"></i>
            `+ service_name + `
        </h4>
        <div class="ui yellow visible message">`+globalFrontendText["operation"]+`: 
            <button class="ui green button tiny" onclick="checkCompile('`+ service_name +`', 0);"><i class="tasks icon"></i>`+globalFrontendText["auto_check"]+`</button>
            <button class="ui blue button tiny" onclick="startPush('`+ service_name +`');"><i class="tasks icon"></i>`+globalFrontendText["submit_code"]+`</button>
            <button class="ui teal button tiny" onClick="startCi('`+ service_name + `','` + globalMemory["task_info"]["feature_branch"] + `')"><i class="tasks icon"></i>`+globalFrontendText["start_ci"]+`</button>
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
                <td>`+ file["code-interpreter"] + `</td>
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

    setTimeout(function () {
        info["files"].forEach(function (file, file_index, file_array) {
            if (file["old-code"].length > 0) {
                mergeCode(file["uuid"], file["code"], file["old-code"], file["code-interpreter"], info["service_name"], file["file-path"])
            } else if (file["code"].length > 0 && typeof file["reference-code"] !== "undefined" && file["reference-code"].length > 0) {
                referenceRepair(file["code"], file["code-interpreter"], file["uuid"], file["reference-file"], info["service_name"], file["file-path"])
            } else {
                checkCode(file["code"], file["code-interpreter"], file["uuid"], file["file-path"], info["service_name"])
            }
        })
    }, 1000);
}

function startPush(serviceName) {
    var requestData = JSON.stringify({ 'service_name': serviceName})

    successCallback = function(data){
        myAlert(globalFrontendText["ok"], data.data)
    }

    sendAjaxRequest('/workspace/gitpush', "POST", requestData, successCallback, alertErrorCallback, true, false)
}

function startCi(repo_path, repo_branch) {  
    customPrompt = "git repo: "+repo_path+", branch: "+repo_branch+", "+globalFrontendText["start_ci"]

    thinkUI(customPrompt, globalFrontendText["ai_think"])
    
    var requestData = JSON.stringify({ 'repo_path': repo_path})

    successCallback = function(data) {
        pluginci(data.data.info)
    }

    sendAjaxRequest('/step_devops/trigger_ci', "POST", requestData, successCallback, aiErrorCallback, true, true)
}

function startCd(repo_path) {  
    customPrompt = globalFrontendText["start_cd"]+": "+repo_path

    thinkUI(customPrompt, globalFrontendText["ai_think"])
    
    var requestData = JSON.stringify({ 'repo_path': repo_path})

    successCallback = function(data) {
        var str = globalFrontendText["start_cd"]+": "+data.data["internet_ip"]
        $(".ai-code").eq($('ai-code').length - 1).html(str);
    }

    sendAjaxRequest('/step_devops/trigger_cd', "POST", requestData, successCallback, aiErrorCallback, true, true)
}

function taskOk(newPrompt, element, operType) {
    var prompt = decodeURI(newPrompt)
    $(element).addClass("disabled");
    $('#prompt-hidePrompt').val(operType);

    $('#prompt-textarea').val(prompt)
    $('#generate-code-button').click()
}

function taskChange(newPrompt, operType) {
    var prompt = decodeURI(newPrompt)
    
    $('#generate-code-button').removeClass("disabled");
    $(".ai-prompt-container").last().children().children().find("textarea").val(prompt);
    globalContext = []
    $('#prompt-hidePrompt').val(operType);
    $('html, body').animate({ scrollTop: $(document).height() }, 'slow');
}

function pluginci(info) {
    if (info["piplineID"]) {
        refreshPluginciStatus(info["piplineID"], info["repopath"], info["piplineUrl"])
    }
}

function refreshPluginciStatus(piplineID, repopath, piplineUrl, element, times) {
    if (typeof times === 'number' && times % 1 === 0) {
        times++
    } else {
        var times=0
    }
    $(element).addClass('loading');
    info = { "piplineID": piplineID, "repopath": repopath }
    $.ajax({
        type: 'GET',
        xhrFields: {
            withCredentials: true
        },
        url: apiUrl + '/step_devops/plugin_ci',
        data: info,
        contentType: 'application/json',
        dataType: 'json'
    }).done(data => {
        if( data.success ) {
            data=data.data
            console.log(data)
            var loadingClass = ""
            if( times < 20 ) {
                loadingClass = "loading"
            }
            var str = `<h4>`+globalFrontendText["start_ci"]+` <div class="ui olive `+loadingClass+` button" onclick="refreshPluginciStatus('` + piplineID + `','` + repopath + `', '`+piplineUrl+`', this, 20)"><i class="sync icon"></i>Update</div><div class="ui blue button" onclick="window.open('`+piplineUrl+`', '_blank');"><i class="tasks icon"></i>View</div></h4><div class="ui middle aligned divided list">`
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

            $(".ai-code").eq($('ai-code').length - 1).html(str);
            // $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
            $('.pluginci-refresh').popup();
            $('.pluginci-status').popup();
            setTimeout(function () {
                if( times < 20 ) {
                    refreshPluginciStatus(piplineID, repopath, piplineUrl, element, times)
                }
            }, 5000);
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

function clarify(customPrompt, thisElement) {
    customPrompt = decodeURI(customPrompt)
    $(thisElement).addClass("disabled");

    thinkUI(customPrompt, globalFrontendText["ai_think"])

    var userName = getParameterByName('userName');
    var requestData = JSON.stringify({ 'user_prompt': customPrompt, 'global_context': JSON.stringify(globalContext) })
    var retruBtn = '<br /><br /><button class="ui green button" onClick="clarify(\''+escapeHtml(customPrompt)+'\', this)">重试</button>'

    successCallback = function(data){
        data = data.data
        globalMemory = data.memory
        var msgJson = data.message
        var msg = JSON.stringify(msgJson)
        var str = ""
        globalContext.push({ role: 'user', content: customPrompt })
        globalContext.push({ role: 'assistant', content: msg })            
        if (msg.includes("development_requirements_overview")) {
            if (msgJson["services_involved"].length > 0) {
                globalChangeServiceList = []
                msgJson["services_involved"].forEach(function (element, element_index, element_array) {
                    globalChangeServiceList.push(element["service-name"])
                })
            } else {
                myAlert(globalFrontendText["error"], globalFrontendText["service_modification_item_empty"])
            }
            msg = globalFrontendText["ai_requirement_clarify_1"]+"\n"+msgJson.development_requirements_overview+"\n\n"+globalFrontendText["ai_requirement_clarify_2"]+"\n"+msgJson.development_requirements_detail
            str = '<br /><br /><button class="ui green button" onClick="taskOk(\''+escapeHtml(msg)+'\', this, \'requirement_doc\')">'+globalFrontendText["submit"]+'</button><button class="ui blue button" onclick="taskChange(\''+escapeHtml(msg)+'\', \'requirement_doc\')">'+globalFrontendText["edit"]+'</button>'
            msg = msg
            msg = '<h5>'+globalFrontendText["ai_requirement_clarify_3"]+'</h5>'+msg
        } else {
            var table = '<h5>'+globalFrontendText["ai_requirement_clarify_4"]+'</h5><table class="ui celled table"><thead><tr><th class="eight wide">'+globalFrontendText["question"]+'</th><th class="eight wide">'+globalFrontendText["answer"]+'</th></tr></thead><tbody>'
            console.log(msgJson)
            msgJson.forEach(function (element, element_index, element_array) {
                table += '<tr><td><span>'+element["question"]+"</span>"+element["reasoning"]+'</td><td><div class="ui fluid icon input"><input type="text" name="clarify_answer" value="'+element["answer_sample"]+'" placeholder="'+globalFrontendText["answer"]+'" autocomplete="off"></div></td></tr>'
            })
            table += '</tbody></table><button class="ui green button" onclick="clarifyOk(this)">'+globalFrontendText["submit"]+'</button>'
            msg = table
        }

        $(".ai-code").eq($('ai-code').length - 1).html(msg.replaceAll('\n', '<br />')+str);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    }

    errorCallback = function(errorMsg) {
        $(".ai-code").eq($('ai-code').length - 1).html(errorMsg+retruBtn);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    }

    sendAjaxRequest('/step_requirement/clarify', "POST", requestData, successCallback, errorCallback, true, true)
}

function genInterfaceDoc(customPrompt, thisElement) {
    customPrompt = decodeURI(customPrompt)
    $(thisElement).addClass("disabled");

    thinkUI(customPrompt, globalFrontendText["ai_think"])

    var requestData = JSON.stringify({ 'user_prompt': customPrompt })
    var retruBtn = '<br /><br /><button class="ui green button" onClick="genInterfaceDoc(\''+escapeHtml(customPrompt)+'\', this)">'+globalFrontendText["retry"]+'</button>'

    successCallback = function(data) {
        data = data.data
        var msg = data.message
        str = "<pre>"+msg+"</pre>"
        str += '<br /><button class="ui green button" onClick="taskOk(\''+escapeHtml(msg)+'\', this, \'api_doc\')">'+globalFrontendText["submit"]+'</button><button class="ui blue button" onclick="taskChange(\''+escapeHtml(msg)+'\', \'api_doc\')">'+globalFrontendText["edit"]+'</button>'

        str = '<h5>'+globalFrontendText["ai_api_clarify_1"]+'</h5><br />'+str
        $(".ai-code").eq($('ai-code').length - 1).html(str);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    }

    errorCallback = function(errorMsg) {
        $(".ai-code").eq($('ai-code').length - 1).html(errorMsg+retruBtn);
        $(".ai-code").eq($('ai-code').length - 1).hide().fadeIn('fast');
    }

    sendAjaxRequest('/step_api/clarify', "POST", requestData, successCallback, errorCallback, true, true)
}

function taskAnalysis(customPrompt, service_name, hideUserPrompt, thisElement) {
    customPrompt = decodeURI(customPrompt)
    $(thisElement).addClass("disabled");

    $('#prompt-textarea').val("");
    $("#prompt-hidePrompt").val("")
    var ai_code_class = service_name.replace("/","-")
    var newField = $('<div class="user-code-container"><div class="ui container grid"><div class="one wide column"><i class="blue  odnoklassniki square icon big" style="font-size: 3em;"></i></div><div class="fifteen wide column ai-content"><div class="ai-code" id="">'+globalFrontendText["ai_api_clarify_confirm"]+'</div></div></div></div> <div class="ai-code-container '+ai_code_class+'"><div class="ui container grid"><div class="one wide column"><i class="orange reddit square icon big" style="font-size: 3em;"></i></div><div class="fifteen wide column ai-content"><div class="ai-code '+ai_code_class+'"><i class="spinner loading icon"></i>'+globalFrontendText["ai_api_subtask_1"]+' '+service_name+' '+globalFrontendText["ai_api_subtask_2"]+'</div></div></div></div>');
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

    var requestData = JSON.stringify({ 'service_name': service_name, 'api_doc': customPrompt })

    var retruBtn = '<br /><br /><button class="ui green button" onClick="taskAnalysis(\''+escapeHtml(customPrompt)+'\',\''+service_name+'\', true, this)">'+globalFrontendText["retry"]+'</button>'

    successCallback = function(data) {
        data = data.data
        var plugin = data.plugin
        globalMemory = data.memory
        if (plugin) {
            triggerPlugin(plugin)
        }
    }

    errorCallback = function(errorMsg) {
        $(".ai-code."+ai_code_class).eq($('.ai-code.'+ai_code_class).length - 1).html(service_name+errorMsg+retruBtn);
    }

    sendAjaxRequest('/step_subtask/analysis', "POST", requestData, successCallback, errorCallback, true, true)
}

function escapeHtml(html) {
  return encodeURI(html.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/g, ' '));
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
