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
        getRenewalList()
        getRechargeList()
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
                        <td><a href="#" onClick="useTenant(`+tenant["tenant_id"]+`)">`+globalFrontendText["enter"]+`: `+tenant["name"]+`</a></td>
                        <td>`+tenant["current_user_role"]+`</td>
                        <td>`+tenant["status_name"]+`</td>
                        <td>`+tenant["member_count"]+`</td>
                        <td>`+tenant["billing_type_name"]+`<br><span style="color:#5b5b5b9e">`+globalFrontendText["tenant_billing_end"]+`: `+tenant["billing_end"]+`</span></td>
                        <td>`+tenant["billing_quota"]+`</td>
                        <td><a href="#" onClick="showTenant(`+tenant["tenant_id"]+`)">`+globalFrontendText["show_tenant"]+`</a> | <a href="setting.html?tenant_id=`+tenant["tenant_id"]+`">`+globalFrontendText["configuration"]+`</a></td>
                    </tr>`
            $("#tenant_list").html(str)
        });
    }

    sendAjaxRequest('/tenant/get_all', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function useTenant(tenant_id) {
    var requestData = JSON.stringify({ 'tenant_id': tenant_id })
 
    successCallback = function(data) {
        window.location.href = "task.html";
    }

    sendAjaxRequest('/tenant/use_tenant?tenant_id='+tenant_id, 'POST', requestData, successCallback, alertErrorCallback, true, false)
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
        $("#current_tenant").text(tenants.name)
        $("#tenant_description").val(tenants.description)
        $("#tenant_employee_count").val(tenants.employee_count)
        $("#tenant_industry_type").val(tenants.industry_type)
        $("#tenant_status").val(tenants.status_name)
        $("#tenant_created_at").val(tenants.created_at)
        $("#tenant_billing_end").val(tenants.billing_end + " - " + tenants.plus_name)
        $("#members_count").text(tenants.member_count)

        $("#renewal_company").text(tenants.name + " | " + tenants.billing_end + " - " + tenants.plus_name)
        $("#recharge_company").text(tenants.name)

        $("#billing_info").text(globalFrontendText["task_limit_msg"] + tenants.billing_quota)
        $("#codepower_info").text(globalFrontendText["code_power"] + tenants.code_power)
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

function Renewal() {
    $('#renewal_plus').modal('show');
}

function Recharge() {
    $('#recharge_cf').modal('show');
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
            expired_at = ""
            code_power = 0
            if (user["bill_type"].startsWith("Income_")) {
                expired_at = "<br /><span style='color:#5b5b5b9e'>"+globalFrontendText["expired_at"]+user["expired_at"]+"</span>"
                code_power = '+' + user["amount"] + '('+user['amount_left']+')' + expired_at
            } else {
                code_power = '-' + user["amount_used"]
            }
            str += `<tr>
                        <td>`+user["bill_type_name"]+`<br /></td>
                        <td>`+user["bill_user"]+`</td>
                        <td>`+code_power+`</td>
                        <td>`+user["created_at"]+`</td>
                        <td><a href="/task.html?task_id=`+user["external_info"]+`">`+user["remarks"]+`</a></td>
                    </tr>`
            $("#bill_list").html(str)
        });
    }

    sendAjaxRequest('/tenant/get_billings', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getRechargeList() {
    var requestData = {}

    successCallback = function(data) {
        code_power = data.data.code_power

        str = `
            <div class="item" style="padding: 10px 20px">
                <div class="right floated content">
                    <div class="ui right labeled input">
                        <input type="number" placeholder="" value=10 id="cf_number">
                        <div class="ui button basic blue pay_btn" onClick="pay_cf('`+data.data.payment_method+`', 'CODE_POWER', this)">
                        <i class="yen sign icon"></i>
                        `+globalFrontendText["recharge"]+`
                        </div>
                    </div>
                </div>
                <i class="chess queen icon yellow big"></i>
                <div class="content">
                `+code_power["value"]+`/`+code_power["key"]+`
                </div>
            </div>
            `
        $("#recharge_list").html(str)
    }

    sendAjaxRequest('/pay/get_price', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function getRenewalList() {
    var requestData = {}

    successCallback = function(data) {
        plus = data.data.plus

        str = `
            <div class="item" style="padding: 10px 20px">
                <div class="right floated content">
                    <div class="ui button blue pay_btn" onClick="pay('`+data.data.payment_method+`', 'BASIC_MONTHLY', this, 'basic_number')"><i class="yen sign icon"></i>`+globalFrontendText["renewal"]+`</div>
                </div>
                <div class="right floated content">
                    <select class="ui fluid dropdown" id="basic_number">
                        <option value="1">1</option>
                        <option value="3">3</option>
                        <option value="6">6</option>
                        <option value="12">12</option>
                    </select>
                </div>
                <i class="chess queen icon yellow big"></i>
                <div class="content">
                `+plus["BASIC_MONTHLY"]["value"]+` / `+plus["BASIC_MONTHLY"]["key"]+` | `+globalFrontendText["task_limit_msg"]+plus["BASIC_MONTHLY"]["billing_quota"]+` | `+globalFrontendText["code_power"]+`: `+plus["BASIC_MONTHLY"]["code_power"] + `
                </div>
            </div>
            <div class="item" style="padding: 10px 20px">
                <div class="right floated content">
                    <div class="ui button blue" onClick="pay('`+data.data.payment_method+`', 'PRO_MONTHLY', this, 'pro_number')"><i class="yen sign icon"></i>`+globalFrontendText["renewal"]+`</div>
                </div>
                <div class="right floated content">
                    <select class="ui fluid dropdown" id="pro_number">
                        <option value="1">1</option>
                        <option value="3">3</option>
                        <option value="6">6</option>
                        <option value="12">12</option>
                    </select>
                </div>
                <i class="chess queen icon orange big"></i>
                <div class="content">
                `+plus["PRO_MONTHLY"]["value"]+` / `+plus["PRO_MONTHLY"]["key"]+` | `+globalFrontendText["task_limit_msg"]+plus["PRO_MONTHLY"]["billing_quota"]+` | `+globalFrontendText["code_power"]+`: `+plus["PRO_MONTHLY"]["code_power"] + `
                </div>
            </div>
            `
        $("#renewal_list").html(str)
    }

    sendAjaxRequest('/pay/get_price', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function pay(payment_method, plus_type, ele, number_id) {
    $(ele).addClass("loading")
    $(ele).addClass("disabled")

    var requestData = JSON.stringify({ 
        'payment_method': payment_method, 
        'plus_type': plus_type,
        'number': parseInt($("#" + number_id).val()),
        'tenant_id': getTenantID(),
    })
 
    successCallback = function(data) {
        window.location.href = data.data
    }

    errorCallback = function(error) {
        $("#invite-message").html(error)
        $("#invite-message").fadeOut().fadeIn()
        $(".pay_btn").removeClass("disabled")
        $(".pay_btn").removeClass("loading")
    }

    sendAjaxRequest('/pay/create_pay', "POST", requestData, successCallback, alertErrorCallback, true, false)
}

function pay_cf(payment_method, plus_type, ele) {
    $(ele).addClass("loading")
    $(ele).addClass("disabled")

    var requestData = JSON.stringify({ 
        'payment_method': payment_method, 
        'tenant_id': getTenantID(),
        'number': parseFloat($("#cf_number").val()),
        'plus_type': plus_type,
    })
 
    successCallback = function(data) {
        window.location.href = data.data
    }

    errorCallback = function(error) {
        $("#invite-message").html(error)
        $("#invite-message").fadeOut().fadeIn()
        $(".pay_btn").removeClass("disabled")
        $(".pay_btn").removeClass("loading")
    }

    sendAjaxRequest('/pay/create_pay', "POST", requestData, successCallback, alertErrorCallback, true, false)
}
