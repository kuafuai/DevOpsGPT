$(document).ready(function () {
    // show dropdown on hover
    $('.ui.dropdown').dropdown({
        on: 'hover'
    });

    const url = window.location;
    const path = url.pathname;
    
    getRechargeList()
});

function getRechargeList() {
    var requestData = {}

    successCallback = function(data) {
        plus = data.data.plus
        $("#intro_pricing_free").text(plus.FREE.suffix+plus.FREE.value)
        $("#intro_pricing_basic").text(plus.BASIC_MONTHLY.suffix+plus.BASIC_MONTHLY.value)
        $("#intro_pricing_pro").text(plus.PRO_MONTHLY.suffix+plus.PRO_MONTHLY.value)

        $("#intro_pricing_free_intro").html(plus.FREE.intro)
        $("#intro_pricing_basic_intro").html(plus.BASIC_MONTHLY.intro)
        $("#intro_pricing_pro_intro").html(plus.PRO_MONTHLY.intro)
    }

    sendAjaxRequest('/pay/get_price', 'GET', requestData, successCallback, alertErrorCallback, true, false)
}

function gotoRegister() {
    url = "/user_register.html?email=" + $("#register-email").val()
    openUrl(url)
}