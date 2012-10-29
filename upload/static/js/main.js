/*
 * jQuery File Upload Plugin JS Example 6.7
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    //$('#fileupload').fileupload();
   //....
   

   $('#fileupload').fileupload()
        .bind('fileuploadsend', function (e, data) {
                /* required info begins */
                var desc = data.context.find("input[name=desc]").val();
		var tag = data.context.find("input[name=tag]").val();
		var pri = data.context.find("input[name=pri]").val();
                //var pubc = data.context.find("select[name=public]").is(':checked');

                //csrf handling is not needed - assuming that jquery ajax is setup with csrf handling.

                if(data.data) { //chrome, ff
                    data.data.append("desc", desc);
                    data.data.append("tag", tag);
		    data.data.append("pri", pri);
		    
                } else { //ie
                    //ie needs separate csrf handling
                    csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

                    data.formData = [{desc:desc, name:"desc", value:desc},
                                     {csrfmiddlewaretoken:csrfmiddlewaretoken,
                                      name: "csrfmiddlewaretoken", value: csrfmiddlewaretoken},
                                     {pri:pri, name:"pri", 
                                      value:pri},
				     {tag:tag, name:"tag", 
                                      value:tag},
                                     ];
                }
                /* required info ends */
            })
        .bind('fileuploaddone', function (e, data) {
                //executed on upload finish of each photo
                if(data.result[0].points_added) { 
                    points_added += data.result[0].points_added; 
                }

            })
        .bind('fileuploadalways', function (e, data) {
                 //executed when upload is completed, whether successfully or unsuccessfully.
                //available vars are
                // data.result
                // data.textStatus;
                // data.jqXHR;
            })
        .bind('fileuploadstop', function (e) {
                 //executed when upload is completed successfully 
            })
        .bind('fileuploadfail', function (e, data) {
                //if file upload fails
                //alert(data.errorThrown);
            })
        .bind('fileuploadadd', function (e, data) {
               // when a file is added/dragged/selected to the uploader 
            });

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );


 
   

    if (window.location.hostname === 'blueimp.github.com') {
        // Demo settings:
        $('#fileupload').fileupload('option', {
            url: '//jquery-file-upload.appspot.com/',
            maxFileSize: 5000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            process: [
                {
                    action: 'load',
                    fileTypes: /^image\/(gif|jpeg|png)$/,
                    maxFileSize: 20000000 // 20MB
                },
                {
                    action: 'resize',
                    maxWidth: 1440,
                    maxHeight: 900
                },
                {
                    action: 'save'
                }
            ]
        });
        // Upload server status check for browsers with CORS support:
        if ($.support.cors) {
            $.ajax({
                url: '//jquery-file-upload.appspot.com/',
                type: 'HEAD'
            }).fail(function () {
                $('<span class="alert alert-error"/>')
                    .text('Upload server currently unavailable - ' +
                            new Date())
                    .appendTo('#fileupload');
            });
        }
    } else {
        // Load existing files:
        $('#fileupload').each(function () {
            var that = this;
            $.getJSON(this.action, function (result) {
                if (result && result.length) {
                    $(that).fileupload('option', 'done')
                        .call(that, null, {result: result});
                }
            });
        });
    }

});






