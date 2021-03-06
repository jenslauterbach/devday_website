"use strict";
function initUploadFields(e, i) {
    var l = e.find("[name=csrfmiddlewaretoken]").val(), a = e.find("[name=upload_url]").val();
    if (!a)return void console.warn("upload_url field is empty; aborting initialization");
    var t = e.find("[name=delete_url]").val(), n = e.find("[name=form_id]").val();
    return n ? void e.find(".file-uploader").each(function (e, d) {
        var o = $(d), r = $(o.find("input[type=file]")), f = o.find(".file-uploader-container"), p = r.attr("name"), m = !!r.attr("multiple"), s = {
            element: f,
            field_name: p,
            csrf_token: l,
            upload_url: a,
            delete_url: t,
            form_id: n,
            multiple: m
        };
        i && $.extend(s, i), m || $(f).on("complete", function () {
            $(o.find(".existing-files")).remove()
        }), initFileUploader(s)
    }) : void console.warn("form_id field is empty; aborting initialization")
}
function initFileUploader(e) {
    var i = $(e.element), l = {
        request: {
            endpoint: e.upload_url,
            params: {csrfmiddlewaretoken: e.csrf_token, field_name: e.field_name, form_id: e.form_id}
        },
        multiple: e.multiple,
        deleteFile: {enabled: !0, endpoint: e.delete_url, method: "POST", customHeaders: {"X-CSRFToken": e.csrf_token}},
        failedUploadTextDisplay: {maxChars: 100, responseProperty: "error", enableTooltip: !0}
    };
    e.text && (l.text = e.text), e.deleteFile && $.extend(l.deleteFile, e.deleteFile), e.failedUploadTextDisplay && $.extend(l.failedUploadTextDisplay, e.failedUploadTextDisplay), e.callbacks && (l.callbacks = e.callbacks), e.template && (l.template = e.template), e.validation && (l.validation = e.validation), i.fineUploader(l);
    var a = i.data("files");
    a && a.forEach(function (e) {
        e.existing || i.fineUploader("addCannedFile", {uuid: e.id, name: e.name})
    })
}