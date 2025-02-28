import {Equipment} from "./equipments/main.js";

$("#newEquipmentModal").on("show.bs.modal", function () {
    const equip = new Equipment()

    equip.loadSelect('equipmentTypeSelect', 'equipmentTypeSelectWrapper',
        'Equipment Type')

    equip.loadSelect('brandSelect', 'brandSelectWrapper', 'Brand')
})
