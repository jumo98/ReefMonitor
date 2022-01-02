checkedCount = 0

$(document).ready(function() {
    $('#input-time').val(moment().format('HH:mm:s'))
    $('#input-date').val(moment().format('yyyy-MM-DD'))

    $('#measurement-sal').change(function() {
        if ($('#measurement-sal').is(':checked')) {
            $('#salinity-input').show()
            checkedCount++
        } else {
            $('#salinity-input').hide()
            checkedCount--
        }

        checkCount()
    });

    $('#measurement-temp').change(function() {
        if ($('#measurement-temp').is(':checked')) {
            $('#temp-input').show()
            checkedCount++
        } else {
            $('#temp-input').hide()
            checkedCount--
        }

        checkCount()
    });

    $('#measurement-carb').change(function() {
        if ($('#measurement-carb').is(':checked')) {
            $('#carb-input').show()
            checkedCount++
        } else {
            $('#carb-input').hide()
            checkedCount--
        }

        checkCount()
    });

    $('#measurement-calcium').change(function() {
        if ($('#measurement-calcium').is(':checked')) {
            $('#calcium-input').show()
            checkedCount++
        } else {
            $('#calcium-input').hide()
            checkedCount--
        }

        checkCount()
    });

    $('#measurement-magnesium').change(function() {
        if ($('#measurement-magnesium').is(':checked')) {
            $('#magnesium-input').show()
            checkedCount++
        } else {
            $('#magnesium-input').hide()
            checkedCount--
        }

        checkCount()
    });

    function checkCount() {
        if (checkedCount <= 0) {
            $('#button-submit').attr('disabled',true);
            $('#timestamp-input').hide()
        } else {
            $('#button-submit').attr('disabled',false);
            $('#timestamp-input').show()
        }
    }

    $("#button-time-now").click(function() {
        $('#input-time').val(moment().format('HH:mm:s'))
        console.log($('#input-time').val())
    });

    $("#button-date-now").click(function() {
        $('#input-date').val(moment().format('yyyy-MM-DD'))
        console.log($('#input-date').val())
    });

    
});