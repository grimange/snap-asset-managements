//Author: RA
//Purpose:  Equipment main js class
//Date: 2/13/2025

import {AMSGlobal} from "../global/main.js";

export class Equipment extends AMSGlobal {
    constructor() {
        super();

    }

    reloadSelect(selectId, selectName) {
        return '<label class="form-label">'+ selectName +'</label>' +
               '<select class="selectpicker search-picker" aria-label="Group" id="'+ selectId +'" disabled>' +
                    '<option value="" selected> </option>'+
               '</select>'
    }
    loadSelect(selectId, selectWrapperId, selectName) {
        const self = this;
        $.ajax({type:'post', url:this.url,
            data:{"select":selectName, "csrfmiddlewaretoken":self.csrftoken},
            beforeSend:function(){
                $("#" + selectWrapperId).empty().html('<i class="fa-solid fa-spinner fa-spin-pulse"></i>')
            },
            success:function(response){
                $("#" + selectWrapperId).empty().html(self.reloadSelect(selectId, selectName))
                const select = $("#" + selectId)
                select.selectpicker('refresh')
                if(Array.isArray(response) && response.length > 0) {
                    select.empty().attr("disabled", false)
                    select.append('<option value="0">Select Equipment Type</option>')
                    response.forEach(element => {
                        select.append('<option value="'+element.id+'">'+element.name+'</option>')
                    });
                    select.selectpicker('refresh')
                }
            },
            error:function(response){
                console.log(response)
            }
        })
    }
}
