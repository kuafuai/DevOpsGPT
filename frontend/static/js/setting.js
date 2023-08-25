$(document).ready(function () {
    getGitConfigList()
    getCIConfigList()
    getCDConfigList()
    getLLMConfigList()

    // show dropdown on hover
    $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
    });
});


function getGitConfigList() {
    requestData = ''

    successCallback = function(data) {
        configs = data.data

        var str = ""

        configs.forEach(function (config, element_index, element_array) {
            str += `<tr style="cursor: pointer;" onClick="showGitConfig(`+config["git_config_id"]+`)">
                        <td>`+config["git_provider"]+`</td>
                        <td>`+config["git_url"]+`</td>
                        <td>`+hideMiddleCharacters(config["git_token"])+`</td>
                        <td>`+config["git_username"]+`</td>
                        <td>`+config["git_email"]+`</td>
                    </tr>`
        });
        $("#git_config_list").html(str)
    }

    sendAjaxRequest('/setting/get_git_config_list', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getCIConfigList() {
    requestData = ''

    successCallback = function(data) {
        configs = data.data

        var str = ""

        configs.forEach(function (config, element_index, element_array) {
            str += `<tr style="cursor: pointer;" onClick="showGitConfig(`+config["ci_config_id"]+`)">
                        <td>`+config["ci_provider"]+`</td>
                        <td>`+config["ci_api_url"]+`</td>
                        <td>`+hideMiddleCharacters(config["ci_token"])+`</td>
                    </tr>`
        });
        $("#ci_config_list").html(str)
    }

    sendAjaxRequest('/setting/get_ci_config_list', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getCDConfigList() {
    requestData = ''

    successCallback = function(data) {
        configs = data.data

        var str = ""

        configs.forEach(function (config, element_index, element_array) {
            str += `<tr style="cursor: pointer;" onClick="showGitConfig(`+config["cd_config_id"]+`)">
                        <td>`+config["cd_provider"]+`</td>
                        <td>`+hideMiddleCharacters(config["ACCESS_KEY"])+`</td>
                        <td>`+hideMiddleCharacters(config["SECRET_KEY"])+`</td>
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
                        <td>`+hideMiddleCharacters(config["llm_key"])+`</td>
                    </tr>`
        });
        $("#llm_config_list").html(str)
    }

    sendAjaxRequest('/setting/get_llm_config_list', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}