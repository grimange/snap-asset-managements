//Author: grimange
//Purpose: Global JS Class
//Date: 3/1/2025

export class AMSGlobal {
    constructor() {
        this.url_equipments = window.location.origin + "/equipments/add/"
        this.url_hr_request = window.location.origin + "/hr/add/"
        this.csrftoken = $("meta[name='csrf-token']").attr("content")
    }
}
