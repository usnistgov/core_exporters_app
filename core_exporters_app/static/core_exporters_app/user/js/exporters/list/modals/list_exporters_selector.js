var data_url_selected = [];
var template_id_list = [];
var template_hash_list = [];

$(document).ready(function() {
    $('#btn-explore-example-export').on('click', exporterSelectionOpenModal);
    $('#btn-exporter-selection-save').on('click', submitExporterSelectionForm);
});


/**
 * Exporter selection form
 */
exporterSelectionOpenModal = function(event) {
    event.preventDefault();
    loadExporterSelectionForm();
};


/**
 * AJAX call, loads exporter selection form
 */
loadExporterSelectionForm = function(){
    // re init the list
    data_url_selected = [];
    template_hash_list = [];
    template_id_list = [];

    $("#results").find(":checked").each(function() {
        data_url_selected.push($(this).val());
        var template_id = $(this).attr("data-template-id");
        var template_hash = $(this).attr("data-template-hash");

        if (template_id) {
            // list of id
            if(template_id_list.indexOf(template_id) < 0){
                template_id_list.push(template_id);
            }
        } else {
            // list of hash
            if(template_hash_list.indexOf(template_hash) < 0){
                template_hash_list.push(template_hash);
            }
        }
    });

    if (data_url_selected.length != 0) {
        $.ajax({
            url: exporterOpenFormUrl,
            type: "POST",
            dataType: "json",
            data: {
                'template_id_list': template_id_list,
                'template_hash_list': template_hash_list,
                'data_url_list': data_url_selected
            },
            success: function (data) {
                $("#select-exporters-modal").modal("show");
                $("#banner_errors").hide();
                $("#form-exporter-selection").html(data.template);
            },
            error: function (data) {
                if (data.responseText != "") {
                    $("#form-exporter-selection-errors").html(data.responseText);
                    $("#banner_errors").show(500);
                    return false;
                }
                return true;
            }
        });
    }else{
        showErrorModal("Please select data to export");
    }
};

/**
 * AJAX call, submit exporter selection form
 */
submitExporterSelectionForm = function(){
    var formData = new FormData($("#form-exporter-selection")[0]);
    formData.append("template_id_list", template_id_list);
    formData.append("template_hash_list", template_hash_list);
    formData.append("data_url_list", data_url_selected);
    // Need to be initialized. window.open not working in asynchronous call (Safari)
    // https://stackoverflow.com/questions/20696041/window-openurl-blank-not-working-on-imac-safari

    var windowReference = window.open();

    $.ajax({
        url : exporterSelectionUrl,
        type : "POST",
        cache: false,
        contentType: false,
        processData: false,
        async: true,
        data: formData,
        success: function(data){
            $("#select-exporters-modal").modal("hide");
            windowReference.location = data.url_to_redirect;
        },
        error:function(data){
            if (data.responseText != ""){
                $("#form-exporter-selection-errors").html(data.responseText);
                $("#banner_errors").show(500);
                return false;
            }
            return true;
        }
    });
};
