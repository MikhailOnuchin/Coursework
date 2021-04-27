

function tag_selected(event){
    var source = event.path[0];
    var type = event.button;
    if(type === 0) {
        var classes = source.classList;
        if(classes.contains('selected_positive')){
            source.classList.remove('selected_positive');
            source.classList.add('selected_negative');
        } else {
            if(classes.contains('selected_negative')) {
                source.classList.remove('selected_negative');
            } else {
                source.classList.add('selected_positive');
            }
        }
    }
}


function toggle_preferences_buttons() {
    var edit_btn = $('#edit_preferences_button')[0];
    var cancel_btn = $('#cancel_edit_preferences_button')[0];
    var save_btn = $('#save_preferences_button')[0];
    if(edit_btn.hidden) {
        edit_btn.hidden = false;
        cancel_btn.hidden = true;
        save_btn.hidden = true;
    } else {
        edit_btn.hidden = true;
        cancel_btn.hidden = false;
        save_btn.hidden = false;
    }
}


function update_tags() {
    var preferences = get_preferences();
    var tags = $('.tag');
    for(var i = 0; i < tags.length; i++) {
        var tag = tags[i];
        var status = preferences[tag.innerText];
        tag.classList.remove('selected_positive', 'selected_negative');
        if(status == 1) {
            tag.classList.add('selected_positive');
        }
        if(status == -1) {
            tag.classList.add('selected_negative');
        }
    }
}


function set_listeners() {
    var tags = $('.tag');
    for(var i = 0; i < tags.length; i++) {
        var tag = tags[i];
        tag.addEventListener('mousedown', tag_selected);
    }
}


function remove_listeners() {
    var tags = $('.tag');
    for(var i = 0; i < tags.length; i++) {
        var tag = tags[i];
        tag.removeEventListener('mousedown', tag_selected);
    }
}


const equals = (a, b) =>
  a.length === b.length &&
  a.every((v, i) => v === b[i]);


function save_preferences() {
    var positive = [];
    var positive_tags = $('.selected_positive');
    for(var i = 0; i < positive_tags.length; i++) {
        positive.push(positive_tags[i].innerHTML);
    }
    var negative = [];
    var negative_tags = $('.selected_negative');
    for(i = 0; i < negative_tags.length; i++) {
        negative.push(negative_tags[i].innerHTML);
    }
    var preferences = {'positive': positive, 'negative': negative};
    console.log(preferences);
    var old_preferences = parse_preferences(get_preferences());
    console.log(old_preferences);
    var equal = equals(old_preferences["positive"], preferences["positive"]) && equals(old_preferences["negative"], preferences["negative"]);
    if(!equal) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/main/set-preferences', false);
        xhr.setRequestHeader('X-CSRFToken', getCSRF());
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send('preferences=' + JSON.stringify(preferences) + '&is_xhr=true');
        console.log(xhr.responseText);
    }
    toggle_preferences_buttons();
    remove_listeners();
}


function clear_preferences() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/main/clear-preferences', false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true');
    console.log(xhr.responseText);
    update_tags();
}


function edit_preferences() {
    toggle_preferences_buttons();
    set_listeners();
}


function cancel_edit_preferences() {
    toggle_preferences_buttons();
    remove_listeners();
    update_tags();
}


function get_preferences() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/main/get-preferences', false);
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('is_xhr=true');
    var preferences = JSON.parse(xhr.responseText);
    return preferences;
}


function parse_preferences(preferences) {
    var positive = [];
    var negative = [];
    for(var [tag, status] of Object.entries(preferences)) {
        if(status == 1) {
            positive.push(tag);
        }
        if(status == -1) {
            negative.push(tag);
        }
    }
    positive.sort()
    negative.sort()
    var res = {'positive': positive, 'negative': negative};
    return res;
}
