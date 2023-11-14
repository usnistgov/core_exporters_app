/*
* button exporter modal js file
*/

var EXPORTER_MAX_RETRY = 30;
var data_url_selected = [];
var template_id_list = [];
var template_hash_list = [];

$(document).ready(function() {
    initExporterModal(0);
});

/**
  * Wait the sharable link in the DOM and create the listeners
  *@param tryCount how many times the function was called
  */
var initExporterModal = function(tryCount) {
    var dataSourceNumber = $(".results-container").length;
    var exporterElement = $('.export-button');
    var notActiveExporterElement = $('.export-button:not(.active)');
    var exporterSelectionElement = $('#btn-exporter-selection-save');
    var paginationElement = $('.pagination li[class != active][class != disabled]');

    if(exporterElement
       && exporterElement.length !== 0
       && exporterElement.length === dataSourceNumber
       && notActiveExporterElement.length > 0) {
        // create click event on the non active download button
        notActiveExporterElement.unbind( "click" );
        notActiveExporterElement.on('click', exporterSelectionOpenModal);
        notActiveExporterElement.addClass('active');
        exporterSelectionElement.unbind( "click" );
        exporterSelectionElement.on('click', submitExporterSelectionForm);

        paginationElement.unbind( "click" );
        paginationElement.on('click', function() { initExporterModal(0); });
    } else if (tryCount < EXPORTER_MAX_RETRY) {
        setTimeout( function(){ initExporterModal(tryCount+1); }, 1000 );
    }
}

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

    $(".result-line-main-container").find(":checked").each(function() {
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
                    $("#form-exporter-selection").html("");
                    $("#select-exporters-modal").modal("show");
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
    var isFormValid = false;
    formData.append("template_id_list", template_id_list);
    formData.append("template_hash_list", template_hash_list);
    formData.append("data_url_list", data_url_selected);

    // at least one of the exporters have to be selected
    $("[name=my_exporters]").each( (index, checkboxElement) => {
        if (checkboxElement.checked)
            isFormValid = true;
    });

    if (isFormValid) {
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
    } else {
        $("#form-exporter-selection-errors").html("No exporter selected.");
        $("#banner_errors").show(500);
    }

};
