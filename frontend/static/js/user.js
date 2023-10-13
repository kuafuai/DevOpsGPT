$(document).ready(function () {
    // show dropdown on hover
    $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
    });

    var queryString = window.location.search;
    var params = new URLSearchParams(queryString);
    $("#login-email").val(params.get('email'));

    $("#login-password").keydown(function (event) {
        if (event.keyCode === 13) {
            // 在这里执行回车键被按下时的操作
            login()
        }
    });
});

function login() {
    var requestData = JSON.stringify({ 'username': $("#login-username").val(), 'password': $("#login-password").val() })
 
    successCallback = function(data) {
        window.location.href = "task.html";
    }

    errorCallback = function(error) {
        $("#login-message").html(error)
        $("#login-message").fadeOut().fadeIn()

        setTimeout(function () {
            $("#login-message").fadeOut();
        }, 4000);
    }

    sendAjaxRequest('/user/login', "POST", requestData, successCallback, errorCallback, true, false)
}

function register() {
    var requestData = JSON.stringify({ 
        'username': $("#login-username").val(), 
        'password': $("#login-password").val(),
        'email': $("#login-email").val(),
        'phone': $("#login-phone").val(),
        'launch_code': $("#login-launch_code").val(),
        'invitation_code': $("#login-invitation-code").val(),
    })
 
    successCallback = function(data) {
        window.location.href = "user_login.html";
    }

    errorCallback = function(error) {
        $("#login-message").html(error)
        $("#login-message").fadeOut().fadeIn()

        setTimeout(function () {
            $("#login-message").fadeOut();
        }, 4000);
    }

    sendAjaxRequest('/user/register', "POST", requestData, successCallback, errorCallback, true, false)
}

function changePassword() {
    var requestData = JSON.stringify({ 
        'password': $("#login-password").val(),
        'phone': $("#login-phone").val(),
        'launch_code': $("#login-launch_code").val(),
    })
 
    successCallback = function(data) {
        window.location.href = "user_login.html";
    }

    errorCallback = function(error) {
        $("#login-message").html(error)
        $("#login-message").fadeOut().fadeIn()

        setTimeout(function () {
            $("#login-message").fadeOut();
        }, 4000);
    }

    sendAjaxRequest('/user/changepassword', "POST", requestData, successCallback, errorCallback, true, false)
}

function send_launch_code(ele, code_type) {
    $(ele).addClass("disabled")
    $(ele).addClass("loading")

    var requestData = JSON.stringify({
        'phone': $("#login-phone").val(),
        'code_type': code_type
    })
 
    successCallback = function(data) {
        $(ele).removeClass("loading")
    }

    errorCallback = function(error) {
        $("#login-message").html(error)
        $("#login-message").fadeOut().fadeIn()
        $(ele).removeClass("loading")
        $(ele).removeClass("disabled")

        setTimeout(function () {
            $("#login-message").fadeOut();
        }, 4000);
    }

    sendAjaxRequest('/user/send_launch_code', "POST", requestData, successCallback, errorCallback, true, false)
}