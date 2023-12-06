$(document).ready(function() {
    function hideInputs() {
        $('#manual-input').hide();
        $('#csv-input').hide();
        $('#submit').hide();
    }

    hideInputs();

    // Show appropriate input fields when radio button is selected
    $('input[type=radio][name=input_type]').change(function() {
        hideInputs();
        $('#' + this.value + '-input').show();
    });

    // Validate input fields before submitting form
    $('#sequence-form').submit(function(event) {
        var isValid = false;

        if ($('#manual').is(':checked')) {
            // Combine sequences across lines to check if all are valid at once
            if (SequenceAlignment.is_valid_dna($('#manual-input').val().replace('\n', ''))) {
                isValid = true;
            }
        }

        if ($('#csv').is(':checked')) {
            var file = $('#csv-input').get(0).files[0];
            if ($('#csv-input').get(0).files[0].type == 'text/csv') {
                isValid = true;
            }
        }

        if (isValid) {
            $('#submit').show();
            event.preventDefault();
        } else {
            event.preventDefault();
        }
    });
});