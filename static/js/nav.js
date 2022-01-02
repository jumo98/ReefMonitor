// $('a[href$="ABC"]')

$(document).ready(function() {
    console.log(window.location.pathname)

    let segments = window.location.pathname.split('/')

    if (segments.length >= 3) {
        button = $("#" + segments[1])
        button.click()
    } 
    
    $("a[href$=\"" + window.location.pathname +"\"]").addClass("active");
})