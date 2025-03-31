import {Equipment} from "./equipments/main.js";
import {HrRequest} from "./hr/main.js";

Object.defineProperty(String.prototype, 'capitalize', {
  value: function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
  },
  enumerable: false
});

$("#newEquipmentModal").on("show.bs.modal", function () {
    const equip = new Equipment()

    equip.loadEquipment()
})

$("#addEquipmentModal").on("hidden.bs.modal", function () {
    $("#newEquipmentModal").modal('show')
})

const newHRRequestModal = $("#newHRRequestModal")

newHRRequestModal.on("show.bs.modal", function () {
    const hr = new HrRequest()

    hr.loadHRRequestCategory()
})

newHRRequestModal.on("hidden.bs.modal", function () {
    $("#newHRRequestNotes").val('')
    $("#files").val('')
})
