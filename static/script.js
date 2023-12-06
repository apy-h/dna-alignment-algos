$(document).ready(function() {
    function hideInputs() {
        $('#manual-input').hide();
        $('#csv-input').hide();
        $('#submit').hide();
    }

    hideInputs();

    // Show appropriate input field (manual or CSV) when radio button is selected
    $('input[type=radio][name=input_type]').change(function() {
        hideInputs();
        $('#' + this.value + '-input').show();
    });

    // Validate input field (manual or CSV) before enabling user to submit form
    $('#manual-input, #csv-input').on('input change', function() {
        $('#submit').hide();

        if ($('#manual').is(':checked')) {
            // Combine sequences across lines to check if all are valid (contain only A, C, G, or T) at once
            if (/^[ACGT]*$/i.test($('#manual-input').val().replace('\n', ''))) {
                $('#submit').show();
            }
        }

        if ($('#csv').is(':checked')) {
            var file = $('#csv-input').get(0).files[0];
            if ($('#csv-input').get(0).files[0].type == 'text/csv') {
                $('#submit').show();
            }
        }
    });
});