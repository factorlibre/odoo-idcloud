odoo.define('pos_idreader_idcloud.screens', function(require){
    "use strict"
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var framework = require('web.framework');
    var _t = core._t;

    var models = require('point_of_sale.models');

    models.load_fields('pos.config', ['idcloud_token', 'idcloud_location']);

    screens.PaymentScreenWidget.include({
        finalize_validation: function() {
            var self = this;
            var order = this.pos.get_order();
            self.send_epc_to_idcloud(order);
            this._super.apply(this, arguments);
        },
        send_epc_to_idcloud: function(order){
            var self = this;
            _.each(order.orderlines.models, function(line) {
                if (line.product_epc !== undefined){
                    var operation = "sell";
                    if (line.qty < 0){
                        operation = 'return';
                    }
                    self.pos.proxy.send_epc_nedap(
                        operation, line.product_epc).then(function(result){
                            console.log('Mark product ' + line.product_epc + ' as ' + operation + ' Response: ' + result['response']);
                        });
                }
            });
        },
    });
})
