$(document).ready(function () {// Define success function
    function replaceStatus(results) {
        var status = results;
        
        if (results) {
            $('#signup').hide();
            $('#status').show().html(status).fadeIn('normal', function() {
                $(this).delay(5000).fadeOut("slow");
               }); //end of fadeIn with its inline anon function
        } else { // end of if results statement and beginning of else statement
            $('#status').show().html("Invalid input, please try again.");
        } //end of else statement

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