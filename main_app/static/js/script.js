// Variables

const dateEl = document.getElementById('id_date');
const selectEl = document.getElementById('id_look_over');
const acquiredEl = document.getElementById('id_date_acquired');


// Sidenav


$(document).ready(function(){
    $('.sidenav').sidenav();
});

$(document).ready(function(){
    $('.materialboxed').materialbox();
});

// Date Picker Animations

M.Datepicker.init(dateEl, {
    format: 'yyyy-mm-dd',
    defaultDate: new Date(),
    setDefaultDate: true,
    autoClose: true
})

M.Datepicker.init(acquiredEl, {
    format: 'yyyy-mm-dd',
    defaultDate: new Date(),
    setDefaultDate: false,
    autoClose: true
})


// Select Widget Animations

M.FormSelect.init(selectEl);