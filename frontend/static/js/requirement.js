$(document).ready(function () {
    getRequirementList()

    // show dropdown on hover
    $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
    });
});

function getRequirementList() {
    requestData = ''

    successCallback = function(data) {
        requirements = data.data.requirements

        var str = ""

        requirements.forEach(function (requirement, element_index, element_array) {
            str += ` <tr style="cursor: pointer;" onClick="showRequirement(`+requirement["requirement_id"]+`)">
                        <td>`+requirement["requirement_id"]+`</td>
                        <td>`+requirement["original_requirement"]+`</td>
                        <td>`+requirement["status"]+`</td>
                        <td>`+requirement["user_id"]+`</td>
                        <td>`+requirement["completion_rating"]+`</td>
                        <td>`+requirement["satisfaction_rating"]+`</td>
                     </tr>
                        `
            $("#app_list").html(str)
        });
    }

    sendAjaxRequest('/requirement/get', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function showRequirement(requirement_id) {
    window.location.href = "/index.html?task_id="+requirement_id
}