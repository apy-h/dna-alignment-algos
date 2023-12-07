$(document).ready(function() {
    // Show tooltip when hovering over cells with overflow
    $('td').each(function() {
        if (this.offsetWidth < this.scrollWidth) {
            $(this).attr('data-toggle', 'tooltip');
            $(this).attr('title', $(this).text());
        }
    });
    $('[data-toggle="tooltip"]').tooltip()
    
    // Hide the manual and CSV input fields and the submit button initally
    hideInputs();

    // Show appropriate input field (manual or CSV) when radio button is selected
    $('input[type=radio][name=input_type]').change(function() {
        hideInputs();
        $('#' + this.value + '-input').show();
    });

    // Validate input field (manual or CSV) before enabling user to submit form
    $('input[type=radio][name=input_type], #manual-input, #csv-input').on('input change', function() {
        $('#submit').hide();
    
        // Combine sequences across lines to check if all are valid (contain only A, C, G, or T) at once for manual input field
        if ($('#manual').is(':checked')) {
            var seqs = $('#manual-input').val()
            if (seqs && /^[ACGT]*$/i.test(seqs.replace(/\n/g, ''))) {
                $('#submit').show();
            }
        }

        // Check if CSV file is valid for CSV input field
        if ($('#csv').is(':checked')) {
            var file = $('#csv-input').get(0).files[0];
            if (file && $('#csv-input').get(0).files[0].type == 'text/csv') {
                $('#submit').show();
            }
        }
    });

    var startTime;

    // Show the loading spinner and start the timer when user presses submit
    $('#submit').click(function() {
        // Show the loading spinner and start the timer
        $('#loading').show();
        $('#loading-spinner').css('animation', 'spin 2s linear infinite');
        startTime = Date.now();
        setInterval(updateTimer, 100); // Update every 100 milliseconds
    });
    
    function updateTimer() {
        var elapsedSeconds = (Date.now() - startTime) / 1000;
        $('#timer').text(elapsedSeconds.toFixed(1) + ' seconds'); // Display 1 decimal place
    }

    function hideInputs() {
        $('#manual-input').hide();
        $('#csv-input').hide();
        $('#submit').hide();
    }
});