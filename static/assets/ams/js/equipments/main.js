//Author: RA
//Purpose:  Equipment main js class
//Date: 2/13/2025

import {AMSGlobal} from "../global/main.js";

export class Equipment extends AMSGlobal {
    constructor() {
        super();

    }

    reloadSelect(selectId, selectName, selectCount = 0) {
        const search = selectCount > 10
        return '<label class="form-label">'+ selectName +'</label>' +
               '<select class="selectpicker search-picker" aria-label="Group" data-live-search="'+ search +'"  id="'+ selectId +'" disabled>' +
                    '<option value="" selected> </option>'+
               '</select>'
    }

    loadAddModal(selectName) {
        const self = this
        const addModal = $("#addEquipmentModal")
        const addLabel = $("#addEquipmentModalLabel")
        const addPartName = $("#addPartName")
        const savePartButton = $("#savePartButton")

        addModal.modal('show')
        addLabel.text("Add " + selectName)

        savePartButton.off('click').on('click', function(){
            if(addPartName.val().length < 2) {
                addPartName.addClass('is-invalid')
                addPartName.focus()
                return false
            }
            else {
                addPartName.removeClass('is-invalid')
            }

            $.ajax({type:'post', url:self.url_equipments,
                data:{"action": "add", 'csrfmiddlewaretoken':self.csrftoken, "name": addPartName.val()},
                beforeSend:function(){
                    addPartName.attr("disabled", true)
                    savePartButton.attr("disabled", true)
                    savePartButton.html('Submit <i class="fa-solid fa-spinner fa-spin-pulse"></i>')
                },
                success:function(response){
                    savePartButton.html('Submit')
                    savePartButton.attr("disabled", false)

                },
                error:function(response){
                    console.log(response)
                }
            })
        })

    }
    loadBrandModel() {
        const self = this
        const equipmentType = $("#equipmentTypeSelect")
        const equipmentBrand = $("#brandSelect")
        const equipmentModel = $("#modelSelect")

        if(equipmentType.val() !== "" && equipmentBrand.val() !== "") {
            equipmentModel.attr("disabled", false)
            $.ajax({type:'post', url:self.url_equipments,
                data:{"action": "get", "select": "Model", "csrfmiddlewaretoken":self.csrftoken, "typeId": equipmentType.val(),
                    "brandId": equipmentBrand.val()},
                beforeSend:function(){

                }, success:function(response){

                }, error:function(response){
                    console.log(response)
                }})
        }
    }
    loadSelect(selectId, selectWrapperId, selectName) {
        const self = this

        $.ajax({type:'post', url:self.url_equipments,
            data:{"select":selectName, "action": "get", "csrfmiddlewaretoken":self.csrftoken},
            beforeSend:function(){
                $("#" + selectWrapperId).empty().html('<i class="fa-solid fa-spinner fa-spin-pulse"></i>')
            },
            success:function(response){
                $("#" + selectWrapperId).empty().html(self.reloadSelect(selectId, selectName, response.length))
                const select = $("#" + selectId)
                select.selectpicker('refresh')
                select.empty().attr("disabled", false)
                select.append('<option value="">Select '+ selectName +'</option>')
                if(Array.isArray(response) && response.length > 0) {
                    response.forEach(element => {
                        select.append('<option value="'+element.id+'">'+element.name.capitalize()+'</option>')
                    });
                }
                select.append('<option value="new" disabled> </option>')
                select.append('<option value="new">Add '+ selectName +'</option>')
                select.selectpicker('refresh')
                select.off('change').on('change', function(){
                    if($(this).val() === "new") {
                        $("#newEquipmentModal").modal('hide')
                        self.loadAddModal(selectName)
                    }
                    else {
                        self.loadBrandModel()
                    }
                })
            },
            error:function(response){
                console.log(response)
            }
        })
    }
}
