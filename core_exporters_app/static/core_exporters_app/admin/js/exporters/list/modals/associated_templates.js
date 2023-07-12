$(document).ready(function() {
    $('.associated-templates').on('click', associatedTemplatesExporterOpenModal);
    $('#form-associated-template-content').on('submit', submit_associated_templates_form);
    $('#btn-associated-templates-save').on('click', submit_associated_templates_form);
});


/**
 * Associated templates selection form
 */
associatedTemplatesExporterOpenModal = function(event) {
    event.preventDefault();
    var exporterId = $(this).parent().attr('id');
    load_associated_templates_form(exporterId);
    $("#select-associated-template-modal").modal("show");
};

/**
 * AJAX call, loads associated template form
 */
load_associated_templates_form = function(exporterId){
    $.ajax({
        url : associatedTemplateUrl,
        type : "GET",
        dataType: "json",
        data : {
            'exporter_id': exporterId
        },
        success: function(data){
            $("#banner_errors").hide();
            $("#form-associated-template-content").html(data.template);
        },
        error:function(data){
            if (data.responseText === "")
                return

            $("#form_associated_templates_errors").html(data.responseText);
            $("#banner_errors").show(500);
        }
    });
};

/**
 * AJAX call, submit associated templates
 */
submit_associated_templates_form = function(){
    var formData = new FormData($("#form-associated-template-content")[0]);
    $.ajax({
        url : associatedTemplateUrl,
        type : "POST",
        cache: false,
        contentType: false,
        processData: false,
        async:true,
        data: formData,
        success: function(data){
            location.reload();
        },
        error:function(data){
            if (data.responseText != ""){
                $("#form_associated_templates_errors").html(data.responseText);
                $("#banner_errors").show(500);
                return (false);
            }
            return (true);
        }
    });
};
