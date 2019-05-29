odoo.define('pos_idreader.screens', function(require){
    "use strict"
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var framework = require('web.framework');
    var _t = core._t;

    screens.ProductScreenWidget.include({
        renderElement: function() {
            this._super.apply(this, arguments);
            var queue = this.pos.proxy_queue;
            var self  = this;

            this.$('.read-rfid-tags').click(function(){
                framework.blockUI();
                var duration = ((self.pos.config.idreader_read_time + 3) * 1000);
                queue.schedule(function(){
                    return self.pos.proxy.rfid_read().then(function(read_results){
                        _.each(read_results, function(product_read){
                            var gtin = product_read.gtin;
                            var ean = gtin.substr(1, gtin.length);
                            self.pos.scan_product({
                                'base_code': ean,
                                'type': 'epc',
                                'value': product_read.epc
                            });
                        });
                    });
                },{duration:duration, repeat:false});
                setTimeout(function(){framework.unblockUI()}, duration);
            });
        }
    })
});
