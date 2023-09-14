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
            str += ` <tr>
                        <td style="cursor: pointer;" onClick="showRequirement(`+requirement["requirement_id"]+`)">`+requirement["requirement_name"]+`<a class="ui `+requirement["status_color"]+` tag label smail">`+requirement["status"]+`</a>
                        <br/ ><div class="description"><i class="green clock icon"></i>`+requirement["created_at"]+`</div>
                        </td>
                        <td class="single line"><a class="ui basic image label">
                        <i class="user blue icon"></i>
                        `+requirement["username"]+`
                      </a></td>
                        <td><div class="ui rating star" data-rating="`+requirement["completion_rating"]+`" rid="`+requirement["requirement_id"]+`" rkey="completion_rating"></div></td>
                        <td><div class="ui rating star" data-rating="`+requirement["satisfaction_rating"]+`" rid="`+requirement["requirement_id"]+`" rkey="satisfaction_rating"></div></td>
                     </tr>
                        `
            $("#app_list").html(str)
        });

        $('.ui.rating').rating({
            maxRating: 5,
            onRate(newValue){
                rid = $(this).attr('rid')
                rkey = $(this).attr('rkey')
                data = {}
                data[rkey] = newValue
                updateRequirment(rid, data)
            }
        });
    }

    sendAjaxRequest('/requirement/get', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function showRequirement(requirement_id) {
    window.location.href = "/task.html?task_id="+requirement_id
}

function updateRequirment(requirement_id, data) {
    var requestData = JSON.stringify({ 'requirement_id': requirement_id, data })

    successCallback = function(data) {
    }

    errorCallback = function(data) {
    }

    sendAjaxRequest('/requirement/update', 'POST', requestData, successCallback, errorCallback, true, false)
}