odoo.define('pos_idreader.devices', function(require){
    "use strict"
    var core = require('web.core');
    var devices = require('point_of_sale.devices');
    devices.ProxyDevice.include({
        // returns reads from RFID scanner
        rfid_read: function(){
            var self = this;
            var output_power = 200;
            var region = 0;
            var timeout = 5;
            if (self.pos.config.idreader_output_power){
                var output_power = self.pos.config.idreader_output_power * 10;
            }
            if (self.pos.config.idreader_region !== undefined){
                var region = self.pos.config.idreader_region;
            }
            if (self.pos.config.idreader_read_time){
                var timeout = self.pos.config.idreader_read_time;
            }
            var ret = new $.Deferred();
            this.message('rfid_read',{output_power: output_power, region: region, timeout: timeout})
                .then(function(result_scans){
                    ret.resolve(result_scans);
                });
            return ret;
        },
        send_epc_nedap: function(operation, epc){
            var self = this;
            var ret = new $.Deferred();
            this.message('epc_send_nedap',{
                    idcloud_token: self.pos.config.idcloud_token,
                    location: self.pos.config.idcloud_location,
                    operation: operation, epc: epc})
                .then(function(result){
                    ret.resolve(result);
                });
            return ret;
        },

    });
});
