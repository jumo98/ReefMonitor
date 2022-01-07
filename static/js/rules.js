let map = {
    "Temperature": "°C",
    "Carbonate Hardness": "KH",
    "Calcium": "ppm",
    "Magnesium": "ppm",
    "Salinity": "mg/l",
}

$(document).ready(function () {
    $("#create-value").html(map[$("#id_parameter").val()])
    $("#edit-value").html(map[$("#id_parameter_create").val()])
})

$("#id_parameter").change(function() {
    $("#create-value").html(map[$("#id_parameter").val()])
});

$("#id_parameter_create").change(function() {
    $("#edit-value").html(map[$("#id_parameter_create").val()])
});