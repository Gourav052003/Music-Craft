

// function preloader(){
//     document.getElementsByClassName("loader").style.display = "none";
//     document.getElementsByClassName("container").style.display = "block";
// }//preloader
// window.onload = preloader;


// ===============================================

// window.preloader = preloader;


// $('document').ready(function(e) {

//     $(".loader").fadeOut("slow"); 
//     }); 

// static/script.js


$(document).ready(function() {
    // Get references to loader container and content
    const loaderContainer = $('#loaderContainer');
    const content = $('.container'); // replace 'content' with the actual ID of your content container

    // Trigger processing function (you can call this when the user uploads music)
    processMusic();

    function processMusic() {
        // Show loader
        loaderContainer.show();

        // Simulate backend processing
        $.ajax({
            type: 'POST',
            url: '/loader',
            success: function(response) {
                // Hide loader and show content when processing is complete
                loaderContainer.hide();
                content.show();
            },
            error: function(error) {
                console.error('Error processing music:', error);
            }
        });

        
    }
});
