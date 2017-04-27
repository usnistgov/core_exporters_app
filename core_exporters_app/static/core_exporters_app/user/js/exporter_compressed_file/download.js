$(document).ready(function() {
    var download_is_ready = $('#download-status').attr('value');
    if(download_is_ready == "False"){
        checkDownloadStatus();
    }
});

/**
 * AJAX call, Check if the file is ready
 */
checkDownloadStatus = function(){
    $.ajax({
        url: checkDownloadUrl,
        type: "GET",
        dataType: "json",
        data: {
            'file_id': $('#download-id').attr('value')
        },
        success: function (data) {
            if(data.is_ready == true){
                $("#download-message").html(data.message);
                // refresh the page and start the download
                location.reload();
            }else{
                // recall the function one second later
                window.setTimeout(checkDownloadStatus, 1000);
            }
        },
        error: function (data) {
            $('#download-message').html('An Error occurred while contacting the server');
        }
    });
};