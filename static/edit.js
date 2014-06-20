$(document).ready(function() {
  $('.edit_button').on('click', function(event) {
    event.preventDefault();
    var id = $(event.target).attr('id')
    $.ajax({
      url: "/_edit/",
      type: 'GET',
      dataType: 'json',
      data: {'id': id},
      context: $(event.target),
      success: function(response) {
        $(event.target).parent().parent().parent().empty().html(response)
      }
    });
  });
});