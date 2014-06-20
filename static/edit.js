$(document).ready(function() {
  $('.edit_entry').on('submit', function(event) {
    event.preventDefault();
    var id = $(event.target).attr('id')
    $.ajax(('/edit/'+id), {
      type: 'GET',
      data: {'id': id},
      context: $(event.target),
      success: function(response) {
        var parent = $(this).parent();
        parent.empty().html(response);
      }
    });
  });
});