var chartColors = {
    salinity: '#0D6EFD',
    temperature: '#6C757D',
    carbonate: '#198754',
    calcium: '#DC3545',
    magnesium: '#FFC107',
};

var init = false;


const options = {
    plugins: {
        legend: {
            display: false
        },
    },
    scales: {
        x: {
            type: 'time',
            grid: {
                // color: "rgba(50, 22, 22,22)",
            }
        },
        y: {
            grid: {
                // color: "rgba(50, 22, 222, 22)",
            }
        }
    }
}

window.onload = function () {
};

$(document).ready(function () {
    $('#input-start-time').val(moment(time_start).format('HH:mm:ss'))
    $('#input-start-date').val(moment(time_start).format('yyyy-MM-DD'))
    $('#input-end-time').val(moment(time_end).format('HH:mm:ss'))
    $('#input-end-date').val(moment(time_end).format('yyyy-MM-DD'))

    $("#button-end-time").click(function () {
        $('#input-end-time').val(moment().format('HH:mm:ss'))
        reload()
    });

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

function reload() {
    start_time = $('#input-start-date').val() + 'T' + $('#input-start-time').val()
    end_time = $('#input-end-date').val() + 'T' + $('#input-end-time').val()
    path = window.location.href.split("?")
    target = path[0] + "?start=" + start_time + "&end=" + end_time
    window.location.replace(target)
}

function loadCharts() {
    parametersJson = JSON.parse(parameters)
    params = {}

    var start = moment(time_start, 'yyyy-MM-DD HH:mm:ss');
    var end = moment(time_end, 'yyyy-MM-DD HH:mm:ss');

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

    configs = []

    for (let [name, param] of Object.entries(params)) {
        let data = {
            labels: param.timestamps,
            datasets: [{
                data: param.values,
                fill: true,
                colors: [],
                cubicInterpolationMode: 'monotone',
                borderColor: chartColors[name],
                // backgroundColor: 'rgb(102, 252, 241)',
                tension: 0.1
            }]
        };

        let config = {
            type: 'line',
            data: data,
            responsive: true,
            // backgroundColor: 'rgb(102, 252, 241)',
            options: options,
        };

        // if (!(init)) {

        // } else {
        //     let myChart = document.getElementById('chart-' + name)
        //     myChart.update();
        // }
        let chartStatus = Chart.getChart('chart-' + name); // <canvas> id
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }

        var ctx = document.getElementById('chart-' + name).getContext('2d');
        let myChart = new Chart(ctx, config);
        myChart.update();

    }
}