$(document).ready(function () {
    parameterUnits = JSON.parse(parameters_units)
    param = $("#id_parameter").val()
    unit = findUnit(param)
    $("#create-value").html(unit)
    $("#edit-value").html(findUnit($("#id_parameter_create").val()))
})

$("#id_parameter").change(function () {
    $("#create-value").html(findUnit($("#id_parameter").val()))
});

$("#id_parameter_create").change(function () {
    $("#edit-value").html(findUnit($("#id_parameter_create").val()))
});

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

