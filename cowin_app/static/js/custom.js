function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


$(document).ready(function(){

    $('#get-otp').prop('disabled', true);
    $('#phone').keyup(function(){
        phone = $('#phone').val()
        if (phone.length != 10){
            $('#phone').addClass('warning-red')
            $('#phone-error').show()
            $('#get-otp').prop('disabled', true);          
        }
        else{
            $('#phone').removeClass('warning-red')
            $('#phone-error').hide()
            $('#get-otp').prop('disabled', false);
        }
        if (phone.length == 0){
            $('#phone').removeClass('warning-red')
            $('#phone-error').hide()
            $('#get-otp').prop('disabled', true);
        }
    })

    $('#get-otp').click(function(){
        phone = $('#phone').val()
        data = {
            'mobile': phone
        }
        $.ajax({
            url: "/get-otp/",
            type: "POST",
            headers: { 'X-CSRFToken': csrftoken },
            data: data,
            success: function(result) {
                $('#otp-div').show();
                $('#change-number').show();
                $('#verify-otp').show();
                $('#verify-otp').prop('disabled', true);
                $('#get-otp').hide();
            }
        });
    })

    $('#otp').keyup(function(){
        otp = $('#otp').val()
        if (otp.length != 6){
            $('#otp').addClass('warning-red')
            $('#otp-error').show()
            $('#otp-error').text("Please enter a 6 digit OTP")
            $('#verify-otp').prop('disabled', true);          
        }
        else{
            $('#otp').removeClass('warning-red')
            $('#otp-error').hide()
            $('#verify-otp').prop('disabled', false);
        }
        if (otp.length == 0){
            $('#otp').removeClass('warning-red')
            $('#otp-error').hide()
            $('#verify-otp').prop('disabled', true);
        }
    })

    $('#verify-otp').click(function(){
        otp = $('#otp').val()
        data = {
            'otp': otp
        }
        $.ajax({
            url: "/verify-otp/",
            type: "POST",
            headers: { 'X-CSRFToken': csrftoken },
            data: data,
            success: function(result) {
                if (result == 200){
                    window.location.href = '/subscribe/'
                }
                else{
                    $('#otp').addClass('warning-red')
                    $('#otp-error').text("Incorrect OTP")
                    $('#otp-error').show()
                }
            }
        });
    })

    $('#states-select').change(function(){
        state_id = $('#states-select').val();
        data = {
            'state_id': state_id
        }
        $.ajax({
            url: "/get-districts/",
            type: "POST",
            headers: { 'X-CSRFToken': csrftoken },
            data: data,
            success: function(result) {
                data = JSON.parse(result)
                $('#district-select').empty()
                $('#district-select').append(`<option value="" selected>Select your district</option>`);
                for(i=0; i<data.length; i++){
                    $('#district-select').append(`<option value="${data[i]['district_id']}">${data[i]['district_name']}</option>`);
                }
            }
        });
    });

    $('#subscribe').prop('disabled', true);
    $('#email').keyup(function(){
        email = $('#email').val()
        var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i
        if (!pattern.test(email)){
            $('#email').addClass('warning-red')
            $('#email-error').show()
            $('#subscribe').prop('disabled', true);
        }
        // else{
        //     $('#email').addClass('warning-red')
        //     $('#email-error').show()
        //     $('#subscribe').prop('disabled', false);
        // }​
        if (!email){
            $('#email').addClass('warning-red')
            $('#email-error').show()
            $('#subscribe').prop('disabled', true);
        }
    });

    $('#subscribe').click(function(){
        district_id = $('#district-select').val()
        email = $('#email').val()
        if (!district_id){
            return
        }
        data = {
            'district_id': district_id
        }
        $.ajax({
            url: "/subscribe/",
            type: "POST",
            headers: { 'X-CSRFToken': csrftoken },
            data: data,
            success: function(result) {
                data = JSON.parse(result)
                $('#district-select').empty()
                $('#district-select').append(`<option value="" selected>Select your district</option>`);
                for(i=0; i<data.length; i++){
                    $('#district-select').append(`<option value="${data[i]['district_id']}">${data[i]['district_name']}</option>`);
                }
            }
        });
    });

});

