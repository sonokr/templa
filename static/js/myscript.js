$('#t_create').click(function (event) {
    $('.tcreate').modal('show');
});

$('#following_button').click(function (event) {
    $('.tcreate').modal('show');
});

$('.ui.modal.tcreate').on('touchmove', function(event) {
    event.stopImmediatePropagation();
})