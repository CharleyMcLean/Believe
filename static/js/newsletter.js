$(document).ready(function () {// Define success function
    function replaceStatus(results) {
        var status = results;
        $('#email-signup').html(status);
        console.log("Finished replaceStatus");
    } //end replaceStatus function

    function updateStatus(evt) {
        evt.preventDefault();
        var name = $('#name').val();
        var email = $('#email').val();
        var zipcode = $('#zipcode').val();

        $.post('/newsletter-signup', {name: name, email: email, zipcode: zipcode}, replaceStatus);
        console.log("Finished sending AJAX");
    } //end updateStatus function
    // debugger;
    $('#email-signup').on('click', updateStatus);

    console.log('hi');
});