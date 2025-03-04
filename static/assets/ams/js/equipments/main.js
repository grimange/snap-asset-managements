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
    reloadInput(inputName, inputValue = "text") {
        return '<div class="mb-3 mt-2 col-md-6">' +
                    '<label class="form-label">'+ inputName +'</label>' +
                    '<input type="text" class="form-control" value="'+ inputValue +'" disabled>' +
               '</div>'
    }

    loadAddModelModal(equipmentTypeId, equipmentTypeName, equipmentBrandId, equipmentBrandName) {
        const self = this
        const addModal = $("#addEquipmentModal")
        const addLabel = $("#addEquipmentModalLabel")
        const RowWrapper = $("#addEquipmentFormWrapperRow")
        const savePartButton = $("#savePartButton")

        addLabel.text("Add Model")
        RowWrapper.empty()
        RowWrapper.append(self.reloadInput('Equipment Type ',  equipmentTypeId + " - " + equipmentTypeName))
        RowWrapper.append(self.reloadInput('Equipment Brand ', equipmentBrandId + " - " + equipmentBrandName))
        RowWrapper.append('<div class="mb-3 mt-2 col-md-6"><label class="form-label">Name</label>' +
                          '<input type="text" class="form-control" id="modelName"></div>')

        const modelName = $("#modelName")
        addModal.modal('show')

        savePartButton.off('click').on('click', function(){
            if(modelName.val().length < 2) {
                modelName.addClass('is-invalid')
                modelName.focus()
                return false
            }
            else {
                modelName.removeClass('is-invalid')
            }
            $.ajax({type:'post', url:self.url_equipments,
                data:{"action": "add", "select": "Model", 'csrfmiddlewaretoken':self.csrftoken,
                    "typeId": equipmentTypeId, "brandId": equipmentBrandId, "name": modelName.val(),
                    "description": " "}, dataType: 'json',
                beforeSend:function(){
                    modelName.attr("disabled", true)
                    savePartButton.attr("disabled", true)
                    savePartButton.html('Submit <i class="fa-solid fa-spinner fa-spin-pulse"></i>')
                },
                success:function(response){
                    modelName.attr("disabled", true)
                    savePartButton.attr("disabled", true)
                    savePartButton.html('Submit')
                    addModal.modal('hide')
                }, error:function(response){
                    console.log(response)
                }
            })
        })

    }
    loadAddModal(selectName) {
        const self = this
        const addModal = $("#addEquipmentModal")
        const addLabel = $("#addEquipmentModalLabel")
        const savePartButton = $("#savePartButton")
        const RowWrapper = $("#addEquipmentFormWrapperRow")

        RowWrapper.empty()
        RowWrapper.append('<div class="mb-3 mt-2 col-md-6">' +
                                '<label class="form-label">Name</label>' +
                                '<input type="text" class="form-control" id="addPartName">' +
                          '</div>')

        const addPartName = $("#addPartName")
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
                data:{"action": "add", "select": selectName, 'csrfmiddlewaretoken':self.csrftoken,
                    "name": addPartName.val()}, dataType: 'json',
                beforeSend:function(){
                    addPartName.attr("disabled", true)
                    savePartButton.attr("disabled", true)
                    savePartButton.html('Submit <i class="fa-solid fa-spinner fa-spin-pulse"></i>')
                },
                success:function(response){
                    addPartName.attr("disabled", false)
                    addPartName.val('')
                    savePartButton.html('Submit')
                    savePartButton.attr("disabled", false)
                    addModal.modal('hide')
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

        if(equipmentType.val() !== "" && equipmentBrand.val() !== "") {
            const equipmentTypeName = equipmentType.find('option:selected').text()
            const equipmentBrandName = equipmentBrand.find('option:selected').text()
            const saveEquipment = $("#saveEquipment")

            $.ajax({type:'post', url:self.url_equipments,
                data:{"action": "get", "select": "Model", "csrfmiddlewaretoken":self.csrftoken,
                    "typeId": equipmentType.val(), "brandId": equipmentBrand.val()}, dataType: 'json',
                beforeSend:function(){
                    $("#modelSelectWrapper").empty().html('<div class="mb-3 mt-2 col-md-6">' +
                                                                '<label class="form-label">Model</label>' +
                                                                '<span class="form-control">' +
                                                                    '<i class="fa-solid fa-spinner fa-spin-pulse"></i>' +
                                                                '</span>' +
                                                          '</div>')
                }, success:function(response){
                    $("#modelSelectWrapper").empty().html(self.reloadSelect('modelSelect', 'Model', response.length))

                    const equipmentModel = $("#modelSelect")
                    equipmentModel.selectpicker('refresh')

                    equipmentModel.attr("disabled", false)
                    equipmentModel.append('<option value="">Select Model</option>')
                    if(Array.isArray(response) && response.length > 0) {
                        response.forEach(element => {
                            equipmentModel.append('<option value="'+element.id+'">' +element.name.capitalize()+ '</option>')
                        })
                    }
                    equipmentModel.append('<option value="" disabled> </option>')
                    equipmentModel.append('<option value="new">Add Model</option>')

                    equipmentModel.selectpicker('refresh')
                    equipmentModel.off('change').on('change', function(){
                        if($(this).val() === "new") {
                            $("#newEquipmentModal").modal('hide')
                            self.loadAddModelModal(equipmentType.val(), equipmentTypeName,
                                equipmentBrand.val(), equipmentBrandName)
                        }
                        else if($(this).val() !== "") {
                            saveEquipment.attr("disabled", false)
                            saveEquipment.text('Submit')
                        }
                        $(this).selectpicker('refresh')
                    })
                }, error:function(response){
                    console.log(response)
                }})
        }
    }
    loadSelect(selectId, selectWrapperId, selectName) {
        const self = this
        $.ajax({type:'post', url:self.url_equipments,
            data:{"select":selectName, "action": "get", "csrfmiddlewaretoken":self.csrftoken}, dataType: 'json',
            beforeSend:function(){
                $("#" + selectWrapperId).empty().html('<div class="mb-3 mt-2 col-md-6">' +
                                                        '<label class="form-label">'+ selectName +'</label>' +
                                                        '<span class="form-control">' +
                                                            '<i class="fa-solid fa-spinner fa-spin-pulse"></i>' +
                                                        '</span>' +
                                                      '</div>')
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
                if(selectName !== "Equipment Type") {
                    select.append('<option value="" disabled> </option>')
                    select.append('<option value="new">Add '+ selectName +'</option>')
                }

                select.selectpicker('refresh')
                select.off('change').on('change', function(){
                    const select2 = $(this)
                    if(select2.val() === "new") {
                        $("#newEquipmentModal").modal('hide')
                        self.loadAddModal(selectName)
                    }
                    else {
                        self.loadBrandModel()
                    }
                    $(this).selectpicker('refresh')
                })
            },
            error:function(response){
                console.log(response)
            }
        })
    }
    loadEquipment() {
        const self = this
        self.loadSelect('equipmentTypeSelect', 'equipmentTypeSelectWrapper', 'Equipment Type')
        self.loadSelect('brandSelect', 'brandSelectWrapper', 'Brand')

        const saveEquipment = $("#saveEquipment")
        saveEquipment.off('click').on('click', function(){
           const equipmentType = $("#equipmentTypeSelect")
           const equipmentBrand = $("#brandSelect")
           const equipmentModel = $("#modelSelect")
           const serialNumber   = $("#serialNumber")

            if(equipmentType.val() === "") {
                equipmentType.addClass('is-invalid')
                equipmentType.focus()
                return false
            }
            else {
                equipmentType.removeClass('is-invalid')
            }

            if(equipmentBrand.val() === "") {
                equipmentBrand.addClass('is-invalid')
                equipmentBrand.focus()
                return false
            }
            else {
                equipmentBrand.removeClass('is-invalid')
            }

            if(equipmentModel.val() === "") {
                equipmentModel.addClass('is-invalid')
                equipmentModel.focus()
                return false
            }
            if(serialNumber.val().length < 2) {
                serialNumber.addClass('is-invalid')
                serialNumber.focus()
                return false
            }
            else {
                serialNumber.removeClass('is-invalid')
            }

            $.ajax({type:'post', url:self.url_equipments, data:{"csrfmiddlewaretoken":self.csrftoken,
                    "action": "add", "select": "Equipment", "modelId": equipmentModel.val(),
                    "serialNumber": serialNumber.val()}, dataType: 'json',
                beforeSend:function(){
                    equipmentType.attr("disabled", true)
                    equipmentBrand.attr("disabled", true)
                    equipmentModel.attr("disabled", true)
                    serialNumber.attr("disabled", true)
                    saveEquipment.attr("disabled", true)
                    saveEquipment.text('Submit <i class="fa-solid fa-spinner fa-spin-pulse"></i>')
                },
                success:function(response){
                    $("#newEquipmentModal").modal('hide')
                    console.log(response)
                },
                error:function(response){
                    console.log(response)
                }
            })
        })
    }
}
