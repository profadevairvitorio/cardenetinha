$(document).ready(function() {
    $('#goalModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var url = button.data('url');
        var modal = $(this);

        if (!url) {
            modal.find('.modal-body').html('<p>Error: Could not find the URL to load the form.</p>');
            return;
        }

        modal.find('.modal-body').html('<p>Loading...</p>');

        $.get(url)
            .done(function(data) {
                modal.find('.modal-body').html(data);
            })
            .fail(function() {
                modal.find('.modal-body').html('<p>Error loading content. Please try again.</p>');
            });
    });

    $(document).on('submit', '#goalModal form', function(event) {
        event.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var modal = $('#goalModal');

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function(response) {
                if (typeof response === 'object' && response.success) {
                    modal.modal('hide');
                    location.reload();
                } else {
                    modal.find('.modal-body').html(response);
                }
            },
            error: function() {
                alert('An error occurred while submitting the form. Please try again.');
            }
        });
    });
});
