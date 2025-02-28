//Author: grimange
//Purpose: Global JS Class
//Date: 3/1/2025

export class AMSGlobal {
    constructor() {
        this.url = "http://ec2-54-66-233-233.ap-southeast-2.compute.amazonaws.com:8000/equipments/add/"
        this.csrftoken = $("meta[name='csrf-token']").attr("content")
    }
}
