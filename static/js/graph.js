// Colors for the charts
var chartColors = {
    "Salinity": '#0D6EFD',
    "Temperature": '#6C757D',
    "Carbonate Hardness": '#198754',
    "Calcium": '#DC3545',
    "Magnesium": '#FFC107',
};

$(document).ready(function () {
    // Parse parameter units
    parameterUnits = JSON.parse(parameters_units_json)
    // Initialize date and time buttons according to passed time
    $('#input-start-time').val(moment(time_start).format('HH:mm:ss'))

    $('#input-start-date').val(moment(time_start).format('yyyy-MM-DD'))
    $('#input-start-date').attr({
        "max": moment(time_end).format('yyyy-MM-DD')
    })

    
    $('#input-end-time').val(moment(time_end).format('HH:mm:ss'))
    $('#input-end-date').val(moment(time_end).format('yyyy-MM-DD'))

    // Button for setting time to now
    $("#button-end-time").click(function () {
        $('#input-end-time').val(moment().format('HH:mm:ss'))
        reload()
    });

    // Button for setting date to now
    $("#button-end-date").click(function () {
        $('#input-end-date').val(moment().format('yyyy-MM-DD'))
        reload()
    });

    $('#input-start-time').change(reload)
    $('#input-start-date').change(reload)
    $('#input-end-time').change(reload)
    $('#input-end-date').change(reload)

    loadCharts()
})

// Reload page with new date set as query params
function reload() {
    start_time = $('#input-start-date').val() + 'T' + $('#input-start-time').val()
    end_time = $('#input-end-date').val() + 'T' + $('#input-end-time').val()
    path = window.location.href.split("?")
    target = path[0] + "?start=" + start_time + "&end=" + end_time
    window.location.replace(target)
}

function loadCharts() {
    // Parse handed over measurement
    parametersJson = JSON.parse(parameters)
    params = {}

    var start = moment(time_start, 'yyyy-MM-DD HH:mm:ss');
    var end = moment(time_end, 'yyyy-MM-DD HH:mm:ss');

    // Parse data into chart.js handleable format
    for (let [param, values] of Object.entries(parametersJson)) {
        values.forEach(datapoint => {
            if (!(param in params)) {
                params[param] = {}
            }
            if (!("values" in params[param])) {
                params[param]["values"] = [NaN]
                params[param]["timestamps"] = [start.toISOString()]
                params[param]["moments"] = [start]
            }
            params[param]["values"].push(datapoint.value)
            params[param]["timestamps"].push(datapoint.timestamp)
            params[param]["moments"].push(datapoint.timestamp)
        })

        params[param]["values"].push(NaN)
        params[param]["timestamps"].push(end.toISOString())
        params[param]["moments"].push(end)
    }

    // Create a chart config for each handled parameter
    for (let [name, param] of Object.entries(params)) {
        let data = {
            labels: param.timestamps,
            datasets: [{
                data: param.values,
                fill: true,
                colors: [],
                cubicInterpolationMode: 'monotone',
                borderColor: chartColors[name],
                backgroundColor: chartColors[name],
                tension: 0.1
            }]
        };

        let config = {
            type: 'line',
            data: data,
            responsive: true,
            options: getOptions(findUnit(name)),
        };

        // Find and destroy old chart, if exists
        let chartStatus = Chart.getChart('chart-' + name); // <canvas> id
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }

        // Create a new chart
        var ctx = document.getElementById('chart-' + name).getContext('2d');
        let myChart = new Chart(ctx, config);
        myChart.update();

    }
}

function findUnit(targetParameter) {
    unit = parameterUnits.find((element) => {
        if (element[0] == targetParameter) {
            return element
        }
    })
    if (unit) {
        return unit[1]
    }
    return "N/A"
}

function getOptions(unit) {
    let options = {
        plugins: {
            legend: {
                display: false
            },
        },
        scales: {
            x: {
                type: 'time',
            },
            y: {
                title: {
                    display: true,
                    text: unit,
                    font: {
                        size: 16
                    }
                }
            }
        }
    }

    return options
}