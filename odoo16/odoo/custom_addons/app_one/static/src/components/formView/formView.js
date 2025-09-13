/* @odoo-module */

import { Component , useState , onWillUnmount} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class FormView extends Component{
    static template = "app_one.FormView";

    setup(){
        this.state = useState({
            name : '',
            postcode : '',
            data_availability : ''
        });
        this.rpc = useService("rpc");
    };

    async createRecord(){
       await this.rpc("/web/dataset/call_kw/", {
           model : 'property',
           method : 'create',
           args : [{
               name : this.state.name,
               postcode : this.state.postcode,
               data_availability : this.state.data_availability
           }],
           kwargs : {}
       });
    };

    async cancel(){
       this.state.name = '';
       this.state.postcode = '' ;
       this.state.data_availability = '';
    };



}