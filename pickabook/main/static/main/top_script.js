
function toggle_description(e) {
    var book = $(e.target).parent().parent().parent();
    var description = book.children('.top-book-description');
    var style = description.css('display');
    if (style=='none') {
        description.show(100);
    }
    else {
        description.hide(100);
    }
    e.target.hidden = true;
    $(e.target).siblings()[0].hidden = false;
}

$('.top-book-button').each(function() {
   $(this)[0].addEventListener('click', toggle_description);
});