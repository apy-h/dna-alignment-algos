$(document).ready(function() {
    // Hide all input fields initially
    $('#individual-inputs').hide();
    $('#copy-paste-input').hide();
    $('#csv-input').hide();
    $('#submit').hide();

    // Show appropriate input fields when radio button is selected
    $('input[type=radio][name=input_type]').change(function() {
        $('#individual-inputs').hide();
        $('#copy-paste-input').hide();
        $('#csv-input').hide();
        $('#submit').hide();

        if (this.value == 'individual') {
            $('#individual-inputs').show();
        } else if (this.value == 'copy-paste') {
            $('#copy-paste-input').show();
        } else if (this.value == 'csv') {
            $('#csv-input').show();
        }
    });

    // Add new input field when previous ones are filled
    $('#individual-inputs').on('input', 'input', function() {
        var allFilled = true;
        $('#individual-inputs input').each(function() {
            if ($(this).val() == '') {
                allFilled = false;
                return false;  // Break out of each loop
            }
        });

        if (allFilled) {
            $('#individual-inputs').append('<input type="text" name="sequence" placeholder="Enter DNA sequence">');
        }
    });

    // Validate input fields before submitting form
    $('#sequence-form').submit(function(event) {
        var isValid = true;

        // Validate individual inputs
        $('#individual-inputs input').each(function() {
            if (!SequenceAlignment.is_valid_dna($(this).val())) {
                isValid = false;
                return false;  // Break out of each loop
            }
        });

        // Validate copy-paste input
        if (isValid && $('#copy-paste').is(':checked')) {
            var sequences = $('#copy-paste-input').val().split('\n');
            for (var i = 0; i < sequences.length; i++) {
                if (!SequenceAlignment.is_valid_dna(sequences[i])) {
                    isValid = false;
                    break;
                }
            }
        }

        // Validate CSV input
        if (isValid && $('#csv').is(':checked')) {
            var file = $('#csv-input').get(0).files[0];
            if (file.type != 'text/csv') {
                isValid = false;
            }
        }

        if (!isValid) {
            event.preventDefault();
        } else {
            $('#submit').show();
        }
    });
});