odoo.define('pos_idreader_return.screens', function(require){
    "use strict"
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var framework = require('web.framework');
    var Model = require('web.DataModel');
    var _t = core._t;

    screens.ProductScreenWidget.include({
        renderElement: function() {
            this._super.apply(this, arguments);
            var queue = this.pos.proxy_queue;
            var self  = this;

            this.$('#read_rfid_return_tags').click(function(){
                framework.blockUI();
                var duration = ((self.pos.config.idreader_read_time + 3) * 1000);
                queue.schedule(function(){
                    self.pos.proxy.rfid_read().then(function(read_results){
                        var epc_list = _.map(read_results, function(result){
                            return result.epc;
                        })
                        if (epc_list.length) {
                            (new Model('pos.order.line')).call('search_line_epc', [epc_list])
                            .fail(function (unused, event) {
                                alert('Connection Error. Try again later !!!!');
                            })
                            .done(function(result){
                                if (result.error !== undefined){
                                    self.gui.show_popup('my_message',{
                                        'title': _t('¡No puede devolver este pedido!'),
                                        'body': result.error,
                                    });
                                    return false;
                                }
                                if (result.order.id === undefined){
                                    self.gui.show_popup('my_message',{
                                        'title': _t('¡No puede devolver este pedido!'),
                                        'body': _t("No se han encontrado ventas con estas etiquetas"),
                                    });
                                    return false;
                                }
                                self.pos.db.order_by_id = {};
                                self.pos.db.order_by_id[result.order.id] = result.order;
                                self.pos.db.line_by_id = {};
                                result.orderlines.forEach(function(line){
                                    self.pos.db.line_by_id[line.id] = line;
                                });
                                self.gui.show_popup('return_products_popup',{
                                    'orderlines': result.orderlines,
                                    'order': result.order,
                                    'is_partial_return': result.is_partial_return
                                });
                            });
                        }
                    });
                },{duration:duration, repeat:false});
                setTimeout(function(){framework.unblockUI()}, duration);
            });
        }
    })
});