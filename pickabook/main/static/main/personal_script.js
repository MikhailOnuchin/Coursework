

function get_book_id(e) {
    return $(e.target).siblings('.book-id')[0].innerText;
}


function recommendation_positive(e) {
    var book_id = get_book_id(e);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/main/recommendation-positive', false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true&book_id=' + book_id);
    if(xhr.responseText == 'ok') {
        $(e.target).parent()[0].hidden = true;
        $(e.target).parent().siblings('.top-book-recommendation-done')[0].hidden = false;
    }
}


function recommendation_negative(e) {
    var book_id = get_book_id(e);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/main/recommendation-negative', false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true&book_id=' + book_id);
    if(xhr.responseText == 'ok') {
        $(e.target).parent()[0].hidden = true;
        $(e.target).parent().siblings('.top-book-recommendation-done')[0].hidden = false;
    }
}

$('.recommendation-positive').each(function() {
   $(this)[0].addEventListener('click', recommendation_positive);
});
$('.recommendation-negative').each(function() {
   $(this)[0].addEventListener('click', recommendation_negative);
});