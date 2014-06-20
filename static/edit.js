$(document).ready(function() {
  $('.edit').on('click', function(event) {
    event.preventDefault();
    var id = $(event.target).attr('id')
    $.ajax({
      url: "/_edit/",
      type: 'GET',
      dataType: 'json',
      data: {'id': id},
      context: $(event.target),
      success: function(response) {
        $('#title').val(response.title);
        $('#text').val(response.text);
        $('#entry_id').val(response.id);
        $('div.which_article').html("Editing article: " + response.id);
      }
    });
  });
});