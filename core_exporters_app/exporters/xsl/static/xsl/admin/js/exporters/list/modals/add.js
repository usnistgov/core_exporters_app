$(document).ready(function() {
    $('.btn-add-xslt-exporter').on('click', addXsltOpenModal);
    $('#form-add-xslt-content').on('submit', submit_xslt_selection_form);
    $('#btn-add-xslt').on('click', submit_xslt_selection_form);
});


/**
 * XSLT selection form
 */
addXsltOpenModal = function(event) {
    event.preventDefault();
    load_xslt_selection_form();
    $("#add-xslt-exporter-modal").modal("show");
};

/**
 * AJAX call, loads XSLT selection form
 */
load_xslt_selection_form = function(){
    $.ajax({
        url : addXsltUrl,
        type : "GET",
        dataType: "json",
        success: function(data){
            $("#banner_errors").hide();
            $("#form-add-xslt-content").html(data.template);
        },
        error:function(data){
            if (data.responseText != ""){
                $("#add-xslt-errors").html(data.responseText);
                $("#banner_errors").show(500);
                return (false);
            }
            return (true);
        }
    });
};

/**
 * AJAX call, submit associated templates
 */
submit_xslt_selection_form = function(){
    var formData = new FormData($("#form-add-xslt-content")[0]);
    $.ajax({
        url : addXsltUrl,
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