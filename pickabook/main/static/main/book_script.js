

const book_id = window.location.href.split('/').slice(-1).pop()


function recommendation_positive() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/main/recommendation-positive', false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true&book_id=' + book_id);
    if(xhr.responseText == 'ok') {
        $('#recommendation_review')[0].hidden = true;
    }
}


function recommendation_negative() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/main/recommendation-negative', false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true&book_id=' + book_id);
    if(xhr.responseText == 'ok') {
        $('#recommendation_review')[0].hidden = true;
    }
}


function toggle_buttons(type) {
    var btns = $('.' + type + '_btns');
    if(btns[0].hidden) {
        btns[0].hidden = false;
        btns[1].hidden = true;
    } else {
        btns[0].hidden = true;
        btns[1].hidden = false;
    }
}


function basic_book_func(btns_type ,url) {
    toggle_buttons(btns_type);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/main/' + url, false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true&book_id=' + book_id);
    return xhr.responseText;
}


function make_finished() {
    var res = basic_book_func('finished', 'make-finished');
    console.log(res);
    ensure_unwanted();
}


function make_unfinished() {
    var res = basic_book_func('finished', 'make-unfinished');
    console.log(res);
}


function make_favourite() {
    var res = basic_book_func('favourite', 'make-favourite');
    console.log(res);
}


function make_unfavourite() {
    var res = basic_book_func('favourite', 'make-unfavourite');
    console.log(res);
}


function make_wanted() {
    var res = basic_book_func('wanted', 'make-wanted');
    console.log(res);
    ensure_unfinished();
}


function make_unwanted() {
    var res = basic_book_func('wanted', 'make-unwanted');
    console.log(res);
}


function ensure_unfinished() {
    var btns = $('.finished_btns');
    if(btns[0].hidden) {
        btns[0].hidden = false;
        btns[1].hidden = true;
    }
}


function ensure_unwanted() {
    var btns = $('.wanted_btns');
    if(btns[0].hidden) {
        btns[0].hidden = false;
        btns[1].hidden = true;
    }
}


function send_review() {
    var xhr = new XMLHttpRequest();
    var rating = $('#review_rating :selected');
    var text = $('#review_text')[0];
    xhr.open('POST', '/main/book-review', false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true&book_id=' + book_id + '&rating=' + rating.text() + '&text=' + text.value);
    if(xhr.responseText == "ok") {
        text.value = '';
    }
    location.reload(true);
}


function validate_review() {
    $('#review_send')[0].disabled = !($('#review_text')[0].value != "" && $('#review_rating :selected').text() != "---");
}

$('#review_text')[0].addEventListener('input', validate_review);
$('#review_rating')[0].addEventListener('change', validate_review);