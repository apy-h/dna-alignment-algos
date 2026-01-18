$(document).ready(function() {
    // Theme: initialize preference (localStorage -> system)
    function applyTheme(theme) {
        const isDark = theme === 'dark';
        document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
        const $btn = $('#theme-toggle');
        if ($btn.length) {
            $btn.attr('aria-pressed', isDark);
            $btn.text(isDark ? '☀️' : '🌙');
            $btn.attr('title', isDark ? 'Switch to light' : 'Switch to dark');
        }

        // Swap logo source based on theme
        const $logo = $('.brand-logo');
        if ($logo.length) {
            const lightSrc = $logo.data('light-src');
            const darkSrc = $logo.data('dark-src');
            $logo.attr('src', isDark ? darkSrc : lightSrc);
        }
    }

    (function initTheme() {
        var stored = localStorage.getItem('theme');
        if (!stored) {
            var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            stored = prefersDark ? 'dark' : 'light';
        }
        applyTheme(stored);
    })();

    $('#theme-toggle').on('click', function() {
        var current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        var next = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', next);
        applyTheme(next);
    });

    // Tab switching
    $('.tab-button').on('click', function() {
        const tab = $(this).data('tab');
        
        // Update active states
        $('.tab-button').removeClass('active');
        $(this).addClass('active');
        
        $('.tab-content').removeClass('active');
        $(`#${tab}-tab`).addClass('active');
    });

    // Show tooltip when hovering over cells with overflow
    $('td').each(function() {
        if (this.offsetWidth < this.scrollWidth) {
            $(this).attr('data-toggle', 'tooltip');
            $(this).attr('title', $(this).text());
        }
    });
    $('[data-toggle="tooltip"]').tooltip();

    // Hide the manual and CSV input fields and the submit button initially
    hideInputs();

    // Show appropriate input field (manual or CSV) when radio button is selected
    $('input[type=radio][name=input_type]').change(function() {
        hideInputs();
        $('#' + this.value + '-input').show();
    });

    // Validate input field (manual or CSV) before enabling user to submit form
    $('input[type=radio][name=input_type], #manual-input, #csv-input').on('input change', function() {
        $('#submit').hide();

        // Combine sequences across lines to check if all are valid (not empty and contains only A, C, G, and T) at once for manual input field
        if ($('#manual').is(':checked')) {
            var seqs = $('#manual-input').val()
            if (seqs && /^[ACGT]*$/i.test(seqs.replace(/\n/g, ''))) {
                $('#submit').show();
            }
        }
        // Check if CSV file is valid for CSV input field
        else if ($('#csv').is(':checked')) {
            var file = $('#csv-input').get(0).files[0];
            if (file && $('#csv-input').get(0).files[0].type == 'text/csv') {
                $('#submit').show();
            }
        }
    });

    var startTime;

    // Show the loading spinner and start the timer when user presses submit
    $('#submit').click(function() {
        // Update loading spinner based on current theme
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const spinnerSrc = isDark ? 
            $('#loading-spinner').data('dark-src') : 
            $('#loading-spinner').data('light-src');
        $('#loading-spinner').attr('src', spinnerSrc);
        
        $('#loading').show();
        $('#loading-spinner').css('animation', 'spin 2s linear infinite');
    });

    function hideInputs() {
        $('#manual-input').hide();
        $('#csv-input').hide();
        $('#submit').hide();
    }

    // Bulk selection functionality
    function updateSelectionCount() {
        const count = $('.row-checkbox:checked').length;
        $('#selection-count').text(`${count} selected`);
        
        // Enable/disable buttons based on selection
        const hasSelection = count > 0;
        $('#delete-selected-button').prop('disabled', !hasSelection);
        $('#export-selected-button').prop('disabled', !hasSelection);
        $('#export-unselected-button').prop('disabled', !hasSelection);
    }

    // Select all checkbox
    $('#select-all-checkbox').on('change', function() {
        $('.row-checkbox').prop('checked', this.checked);
        updateSelectionCount();
    });

    // Individual row checkboxes
    $(document).on('change', '.row-checkbox', function() {
        updateSelectionCount();
        
        // Update select-all checkbox state
        const total = $('.row-checkbox').length;
        const checked = $('.row-checkbox:checked').length;
        $('#select-all-checkbox').prop('checked', total === checked);
    });

    // Select all button
    $('#select-all-button').on('click', function() {
        $('.row-checkbox').prop('checked', true);
        $('#select-all-checkbox').prop('checked', true);
        updateSelectionCount();
    });

    // Deselect all button
    $('#deselect-all-button').on('click', function() {
        $('.row-checkbox').prop('checked', false);
        $('#select-all-checkbox').prop('checked', false);
        updateSelectionCount();
    });

    // Delete single row
    $(document).on('click', '.delete-row-button', function() {
        const rowId = $(this).data('row-id');
        
        if (confirm('Are you sure you want to delete this row?')) {
            $.ajax({
                url: `/delete_row/${rowId}`,
                method: 'POST',
                success: function() {
                    location.reload();
                },
                error: function() {
                    alert('Error deleting row');
                }
            });
        }
    });

    // Delete selected rows
    $('#delete-selected-button').on('click', function() {
        const selectedIds = $('.row-checkbox:checked').map(function() {
            return $(this).data('row-id');
        }).get();
        
        const count = selectedIds.length;
        if (confirm(`Delete ${count} selected item${count !== 1 ? 's' : ''}?`)) {
            $.ajax({
                url: '/delete_selected',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ rowIds: selectedIds }),
                success: function() {
                    location.reload();
                },
                error: function() {
                    alert('Error deleting selected rows');
                }
            });
        }
    });

    // Clear database
    $('#clear-database-button').on('click', function() {
        if (confirm('Are you sure you want to clear the entire database? This action cannot be undone.')) {
            $.ajax({
                url: '/clear_database',
                method: 'POST',
                success: function() {
                    location.reload();
                },
                error: function() {
                    alert('Error clearing database');
                }
            });
        }
    });

    // Export selected
    $('#export-selected-button').on('click', function() {
        const selectedIds = $('.row-checkbox:checked').map(function() {
            return $(this).data('row-id');
        }).get();
        
        $.ajax({
            url: '/download_selected',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ rowIds: selectedIds }),
            xhrFields: {
                responseType: 'blob'
            },
            success: function(blob) {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'selected_results.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            },
            error: function() {
                alert('Error exporting selected rows');
            }
        });
    });

    // Export unselected
    $('#export-unselected-button').on('click', function() {
        const selectedIds = $('.row-checkbox:checked').map(function() {
            return $(this).data('row-id');
        }).get();
        
        $.ajax({
            url: '/download_except_selected',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ rowIds: selectedIds }),
            xhrFields: {
                responseType: 'blob'
            },
            success: function(blob) {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'unselected_results.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            },
            error: function() {
                alert('Error exporting unselected rows');
            }
        });
    });
});