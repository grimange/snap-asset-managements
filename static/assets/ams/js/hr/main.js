//Author: RA
//Purpose: Human Resource Request JS Class
//Date: 3/19/2025

import {AMSGlobal} from "../global/main.js";

export class HrRequest extends AMSGlobal {
    constructor() {
        super();
    }
    bytes_to_mb(size_bytes) {
        const size_kb = size_bytes / 1024;
        return Math.round(size_kb / 1024);
    }
    loadsaveNewHRRequest() {
        const self = this
        const savedButton = $("#saveNewHRRequest")
        const attachFiles = $("#files")
        const newHRRequestModal = $("#newHRRequestModal")

        savedButton.off("click").on("click", function () {
            const selectCategory = $("select[name=newHRRequestCategory]")
            const notes = $("#newHRRequestNotes")
            const button = $(this)

            if (selectCategory.val() === "") {
                selectCategory.attr('class', 'form-control is-invalid').focus()
                return false
            }
            else {
                selectCategory.attr('class', 'form-control is-valid')
            }

            if (notes.val() === "") {
                notes.focus()
                return false
            }

            const formData = new FormData()
            const files = attachFiles[0].files
            let total_size = 0

            if(files.length > 0 ) {
                for (let i = 0; i < files.length; i++) {
                    formData.append("files", files[i])
                    total_size += files[i].size
                }
            }

            if(self.bytes_to_mb(total_size) > 50) {
                attachFiles.attr('class', 'form-control is-invalid')
                attachFiles.focus()
                return false
            }
            else {
                attachFiles.attr('class', 'form-control is-valid')
            }

            formData.append('action', 'new_HrRequest')
            formData.append('sub_category_id', selectCategory.val())
            formData.append('notes', notes.val())
            formData.append('csrfmiddlewaretoken', self.csrftoken)

            $.ajax({type:'post',
                    url:self.url_hr_request,
                    data:formData,
                    contentType: false,
                    processData: false,
                    beforeSend: function () {
                        selectCategory.attr("disabled", true)
                        notes.attr("disabled", true)
                        button.html('Submit <i class="fas fa-spin fa-spinner"></i>').attr("disabled", true)
                        attachFiles.attr("disabled", true)
                    }, success: function (response) {
                        newHRRequestModal.modal('hide')
                        button.text('Submit').attr("disabled", false)
                        console.log(response)
                    }, error: function (xhr, status, error) {
                        console.log(xhr)
                        console.log(status)
                        console.log(error)
                    }
            })
        })
    }
    loadHRRequestCategory() {
        const self = this
        const selectCategory = $("select[name=newHRRequestCategory]")
        const savedButton = $("#saveNewHRRequest")

        $.ajax({type:'post', url:self.url_hr_request,
            data:{'csrfmiddlewaretoken': self.csrftoken, 'action': 'load_category'}, dataType: 'json',
            beforeSend:function(){

            },
            success:function(response){
                selectCategory.empty()
                if(Array.isArray(response) && (response.length > 0)){
                    selectCategory.append("<option value=''>Select Category</option>");
                    response.forEach(function(data){
                        if(Array.isArray(data.subs) && data.subs.length > 0){
                            const select = $('<optgroup label="'+ data.category.name +'"></optgroup>')
                            data.subs.forEach(function(sub){
                                if(sub.clickable) {
                                    select.append('<option value="'+sub.id+'">'+sub.name+'</option>')
                                }
                                else {
                                    select.append('<option value="'+sub.id+'" disabled>'+sub.name+'</option>')
                                }
                            })
                            selectCategory.append(select)
                        }
                    })
                    savedButton.attr("disabled", false)
                    self.loadsaveNewHRRequest()
                }
            },
            error:function(response){
                console.log(response);
            }
        })
    }
}
