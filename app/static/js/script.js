/*$('#input_starttime').pickatime({
    // 12 or 24 hour
    twelvehour: true,
});
*/

$(".custom-file-input").on("change", function () {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});