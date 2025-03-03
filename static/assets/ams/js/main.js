import {Equipment} from "./equipments/main.js";

Object.defineProperty(String.prototype, 'capitalize', {
  value: function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
  },
  enumerable: false
});

$("#newEquipmentModal").on("show.bs.modal", function () {
    const equip = new Equipment()

    equip.loadSelect('equipmentTypeSelect', 'equipmentTypeSelectWrapper',
        'Equipment Type')

    equip.loadSelect('brandSelect', 'brandSelectWrapper', 'Brand')
})

$("#addEquipmentModal").on("hidden.bs.modal", function () {
    $("#newEquipmentModal").modal('show')
})

