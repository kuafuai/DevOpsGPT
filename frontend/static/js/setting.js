gitconfigs = []
ciconfigs = []
cdconfigs = []

$(document).ready(function () {
    getGitConfigList()
    getCIConfigList()
    getCDConfigList()
    const url = window.location;
    const path = url.pathname;
    if (path != "/app.html") {
        getTenant(getTenantID())
    }
    //getLLMConfigList()

    // show dropdown on hover
    $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
    });
});

function hideModal(md) {
    $('#'+md).modal('hide');
}

function editGit() {
    var requestData = { 
        'tenant_id': getTenantID(),
        'git_provider': $("#git_provider").val(),
        'git_name': $("#git_name").val(),
        'git_url': $("#git_url").val(),
        'git_token': $("#git_token").val(),
        'git_username': $("#git_username").val(),
        'git_email': $("#git_email").val(),
        'git_config_id': $("#git_config_id").val(),
    }
    requestData = JSON.stringify(requestData)

    successCallback = function(data) {
        location.reload();
    }

    sendAjaxRequest('/setting/edit_git', 'POST', requestData, successCallback, alertErrorCallback, true, false)
}

function showGitConfig(idx) {
    $('#git-edit').modal('show');
    data = gitconfigs[idx]

    $("#git_name").val(data.name)
    $("#git_config_id").val(data.git_config_id)
    $("#git_email").val(data.git_email)
    $("#git_username").val(data.git_username)
    $("#git_token").val(data.git_token)
    $("#git_url").val(data.git_url)
    $("#git_provider").val(data.git_provider)
}

function editCI() {
    var requestData = { 
        'tenant_id': getTenantID(),
        'ci_name': $("#ci_name").val(),
        'ci_provider': $("#ci_provider").val(),
        'ci_api_url': $("#ci_api_url").val(),
        'ci_token': $("#ci_token").val(),
        'ci_config_id': $("#ci_config_id").val(),
    }
    requestData = JSON.stringify(requestData)

    successCallback = function(data) {
        location.reload();
    }

    sendAjaxRequest('/setting/edit_ci', 'POST', requestData, successCallback, alertErrorCallback, true, false)
}

function showCIConfig(idx) {
    $('#ci-edit').modal('show');
    data = ciconfigs[idx]

    $("#ci_name").val(data.name)
    $("#ci_config_id").val(data.ci_config_id)
    $("#ci_api_url").val(data.ci_api_url)
    $("#ci_token").val(data.ci_token)
    $("#ci_provider").val(data.ci_provider)
}

function editCD() {
    var requestData = { 
        'tenant_id': getTenantID(),
        'cd_name': $("#cd_name").val(),
        'cd_provider': $("#cd_provider").val(),
        'ACCESS_KEY': $("#ACCESS_KEY").val(),
        'SECRET_KEY': $("#SECRET_KEY").val(),
        'cd_config_id': $("#cd_config_id").val(),
    }
    requestData = JSON.stringify(requestData)

    successCallback = function(data) {
        location.reload();
    }

    sendAjaxRequest('/setting/edit_cd', 'POST', requestData, successCallback, alertErrorCallback, true, false)
}

function showCDConfig(idx) {
    $('#cd-edit').modal('show');
    data = cdconfigs[idx]

    $("#cd_name").val(data.name)
    $("#cd_config_id").val(data.cd_config_id)
    $("#cd_provider").val(data.cd_provider)
    $("#ACCESS_KEY").val(data.access_key)
    $("#SECRET_KEY").val(data.secret_key)
}


function getGitConfigList() {
    requestData = {'tenant_id': getTenantID()}

    successCallback = function(data) {
        gitconfigs = data.data

        var str = ""

        gitconfigs.forEach(function (config, element_index, element_array) {
            str += `<tr style="cursor: pointer;" onClick="showGitConfig(`+element_index+`)">
                        <td>`+config["name"]+`</td>
                        <td>`+config["git_provider"]+`</td>
                        <td>`+config["git_url"]+`</td>
                        <td>`+config["git_token"]+`</td>
                        <td>`+config["git_username"]+`</td>
                        <td>`+config["git_email"]+`</td>
                    </tr>`
        });
        $("#git_config_list").html(str)
    }

    sendAjaxRequest('/setting/get_git_config_list', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getCIConfigList() {
    requestData = {'tenant_id': getTenantID()}

    successCallback = function(data) {
        ciconfigs = data.data

        var str = ""

        ciconfigs.forEach(function (config, element_index, element_array) {
            str += `<tr style="cursor: pointer;" onClick="showCIConfig(`+element_index+`)">
                        <td>`+config["name"]+`</td>
                        <td>`+config["ci_provider"]+`</td>
                        <td>`+config["ci_api_url"]+`</td>
                        <td>`+config["ci_token"]+`</td>
                    </tr>`
        });
        $("#ci_config_list").html(str)
    }

    sendAjaxRequest('/setting/get_ci_config_list', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getCDConfigList() {
    requestData = {'tenant_id': getTenantID()}

    successCallback = function(data) {
        cdconfigs = data.data

        var str = ""

        cdconfigs.forEach(function (config, element_index, element_array) {
            str += `<tr style="cursor: pointer;" onClick="showCDConfig(`+element_index+`)">
                        <td>`+config["name"]+`</td>
                        <td>`+config["cd_provider"]+`</td>
                        <td>`+config["ACCESS_KEY"]+`</td>
                        <td>`+config["SECRET_KEY"]+`</td>
                    </tr>`
        });
        $("#cd_config_list").html(str)
    }

    sendAjaxRequest('/setting/get_cd_config_list', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getLLMConfigList() {
    requestData = ''

    successCallback = function(data) {
        configs = data.data

        var str = ""

        configs.forEach(function (config, element_index, element_array) {
            str += `<tr style="cursor: pointer;" onClick="showGitConfig(`+config["llm_config_id"]+`)">
                        <td>`+config["llm_provider"]+`</td>
                        <td>`+config["llm_api_url"]+`</td>
                        <td>`+config["llm_api_version"]+`</td>
                        <td>`+config["llm_api_proxy"]+`</td>
                        <td>`+hideMiddleCharacters(config["llm_key"], 2)+`</td>
                    </tr>`
        });
        $("#llm_config_list").html(str)
    }

    sendAjaxRequest('/setting/get_llm_config_list', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function addGitConfig() {
    cleanUp()
    $('#git-edit').modal('show');
}

function addCIConfig() {
    cleanUp()
    $('#ci-edit').modal('show');
}

function addCDConfig() {
    cleanUp()
    $('#cd-edit').modal('show');
}

function cleanUp() {
    $("#git_config_id").val('')
    $("#git_email").val('')
    $("#git_username").val('')
    $("#git_token").val('')
    $("#git_url").val('')
    $("#git_provider").val('')

    $("#ci_config_id").val('')
    $("#ci_api_url").val('')
    $("#ci_token").val('')
    $("#ci_provider").val('')

    $("#cd_config_id").val('')
    $("#cd_provider").val('')
    $("#ACCESS_KEY").val('')
    $("#SECRET_KEY").val('')

    $("#git_name").val('')
    $("#ci_name").val('')
    $("#cd_name").val('')
}
