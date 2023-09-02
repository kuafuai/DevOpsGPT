$(document).ready(function () {
    // show dropdown on hover
    $('.ui.dropdown').dropdown({
        on: 'hover'
    });

    

    const url = window.location;
    const path = url.pathname;
    if (path == "/tenant_detail.html") {
        var tenant_id = getTenantID();
        getTenant(tenant_id)
        getTenantMembers(tenant_id)
        getBillings(tenant_id)
    }

    if (path == "/tenant.html") {
        getTenantList()
    }
});

function tenantSubmit() {
    var requestData = JSON.stringify({ 
        'name': $("#tenant_name").val(), 
        'description': $("#tenant_description").val(),
        'country': $("#tenant_country").val(),
        'industry_type': $("#tenant_industry_type").val(),
        'employee_count': $("#tenant_employee_count").val(),
    })
 
    successCallback = function(data) {
        window.location.href = "tenant.html";
    }

    errorCallback = function(error) {
        $("#login-message").html(error)
        $("#login-message").fadeOut().fadeIn()
    }

    sendAjaxRequest('/tenant/create', "POST", requestData, successCallback, errorCallback, true, false)
}

function getTenantList() {
    requestData = ''

    successCallback = function(data) {
        tenants = data.data

        var str = ""

        tenants.forEach(function (tenant, element_index, element_array) { 
            str += `<tr>
                        <td>`+tenant["name"]+`<br /></td>
                        <td>`+tenant["current_user_role"]+`</td>
                        <td>`+tenant["status"]+`</td>
                        <td>`+tenant["member_count"]+`</td>
                        <td>`+tenant["billing_type"]+`</td>
                        <td>`+tenant["billing_quota"]+`</td>
                        <td>`+tenant["billing_end"]+`</td>
                        <td><a href="#" onClick="useTenant(`+tenant["tenant_id"]+`)">`+globalFrontendText["enter"]+`</a> | <a href="#" onClick="showTenant(`+tenant["tenant_id"]+`)">`+globalFrontendText["show_tenant"]+`</a> | <a href="setting.html?tenant_id=`+tenant["tenant_id"]+`">`+globalFrontendText["configuration"]+`</a></td>
                    </tr>`
            $("#tenant_list").html(str)
        });
    }

    sendAjaxRequest('/tenant/get_all', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function useTenant(tenant_id) {
    var requestData = JSON.stringify({ 'tenant_id': tenant_id })
 
    successCallback = function(data) {
        window.location.href = "index.html";
    }

    sendAjaxRequest('/tenant/use_tenant', 'POST', requestData, successCallback, alertErrorCallback, true, false)
}

function showTenant(tenant_id) {
    window.location.href = "tenant_detail.html?tenant_id="+tenant_id;
}

function getTenant(tenant_id) {
    var requestData = { 'tenant_id': tenant_id }

    successCallback = function(data) {
        tenants = data.data

        $("#tenant_country").val(tenants.country)
        $("#tenant_name").val(tenants.name)
        $("#tenant_description").val(tenants.description)
        $("#tenant_employee_count").val(tenants.employee_count)
        $("#tenant_industry_type").val(tenants.industry_type)
        $("#tenant_status").val(tenants.status)
        $("#tenant_created_at").val(tenants.created_at)
        $("#tenant_billing_end").val(tenants.billing_end)
        $("#members_count").text(tenants.member_count)

        $("#billing_info").text(tenants.billing_quota+"/"+tenants.billing_type)
    }

    sendAjaxRequest('/tenant/get_one', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getTenantMembers(tenant_id) {
    var requestData = { 'tenant_id': tenant_id }

    successCallback = function(data) {
        users = data.data

        var str = ""

        users.forEach(function (user, element_index, element_array) { 
            str += `<tr>
                        <td>`+user["username"]+`<br /></td>
                        <td>`+user["current_user_role"]+`</td>
                        <td>`+user["status"]+`</td>
                        <td>`+hideMiddleCharacters(user["email"], 2)+`</td>
                        <td>`+hideMiddleCharacters(user["phone_number"], 1.5)+`</td>
                    </tr>`
            $("#user_list").html(str)
        });
    }

    sendAjaxRequest('/tenant/get_members', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function addMember() {
    $('#add_member').modal('show');
}

function invite() {
    $("#invite_btn").addClass("disabled")
    $("#invite_btn").addClass("loading")

    var requestData = JSON.stringify({ 
        'email': $("#invite_email").val(), 
        'role': $("#invite_role").val(),
        'tenant_id': getTenantID(),
    })
 
    successCallback = function(data) {
        location.reload()
    }

    errorCallback = function(error) {
        $("#invite-message").html(error)
        $("#invite-message").fadeOut().fadeIn()
        $("#invite_btn").removeClass("disabled")
        $("#invite_btn").removeClass("loading")
    }

    sendAjaxRequest('/tenant/invite', "POST", requestData, successCallback, errorCallback, true, false)
}

function getBillings(tenant_id) {
    var requestData = { 'tenant_id': tenant_id }

    successCallback = function(data) {
        users = data.data

        var str = ""

        users.forEach(function (user, element_index, element_array) { 
            str += `<tr>
                        <td>`+user["bill_type"]+`<br /></td>
                        <td>`+user["bill_user"]+`</td>
                        <td>`+user["created_at"]+`</td>
                        <td><a href="/?task_id=`+user["external_info"]+`">`+user["remarks"]+`</a></td>
                    </tr>`
            $("#bill_list").html(str)
        });
    }

    sendAjaxRequest('/tenant/get_billings', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}