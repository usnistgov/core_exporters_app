$(document).ready(function() {
    $('.edit').on('click', editExporterOpenModal);
    $('#edit-exporter-form').on('submit', editExporterSave);
    $('#edit-exporter-save').on('click', editExporterSave);
});


/**
 * Edit general information of an exporter
 */
editExporterOpenModal = function(event) {
    event.preventDefault();

    var exporterName = $(this).parent().siblings(':first').text();
    var exporterId = $(this).parent().attr('id');

    $("#edit-exporter-name").val(exporterName);
    $("#edit-exporter-id").val(exporterId);
    $("#edit-exporter-modal").modal("show");
};

/**
 * Save general information of an exporter
 */
editExporterSave = function(event) {
    event.preventDefault();

    var exporterId = $("#edit-exporter-id").val();
    var exporterName = $("#edit-exporter-name").val();

    $.ajax({
        url : editExporterPostUrl,
        type : "POST",
        data: {
            "id": exporterId,
            "title": exporterName
        },
        success: function(data){
            location.reload();
        }
    });
};
