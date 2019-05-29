odoo.define('pos_idreader.models', function(require){
    "use strict"
    var core = require('web.core');
    var _t = core._t;

    var models = require('point_of_sale.models');

    models.load_fields('pos.config', ['iface_idreader', 'idreader_region', 'idreader_output_power', 'idreader_read_time']);
    models.load_fields('pos.order.line', 'product_epc');

    var _pos_config = _.findWhere(
        models.PosModel.prototype.models,
        {model: "pos.config"}
    );

    var _pos_config_loaded = _pos_config.loaded;
    _pos_config.loaded = function (self, configs){
        _pos_config_loaded.apply(this, arguments);
        self.config.use_proxy = self.config.use_proxy ||
                                self.config.iface_idreader;
    };

    var _orderline_super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        can_be_merged_with: function(orderline){
            var result = _orderline_super.can_be_merged_with.apply(this, arguments);
            if (this.product_epc !== orderline.product_epc){
                result = false;
            }
            return result;
        },
        set_product_epc: function(epc){
            this.order.assert_editable();
            this.product_epc = epc;
            this.trigger('change',this);
        },
        export_as_JSON: function() {
            var result = _orderline_super.export_as_JSON.apply(this, arguments);
            result['product_epc'] = this.product_epc;
            return result
        }
    });

    models.Order = models.Order.extend({
        add_product_epc: function(product, options){
            if(this._printed){
                this.destroy();
                return this.pos.get_order().add_product(product, options);
            }
            this.assert_editable();
            options = options || {};
            var attr = JSON.parse(JSON.stringify(product));
            attr.pos = this.pos;
            attr.order = this;

            if (options.epc !== undefined) {
                // Do no add orderline if the order has one line created with the same EPC
                var orderlines = this.orderlines.models;
                for(var i = 0; i < orderlines.length; i++){
                    if(orderlines[i].product_epc !== undefined && orderlines[i].product_epc === options.epc){
                        return null;
                    }
                }
            }

            var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});

            if(options.quantity !== undefined){
                line.set_quantity(options.quantity);
            }

            if(options.price !== undefined){
                line.set_unit_price(options.price);
            }

            if(options.epc !== undefined){
                line.set_product_epc(options.epc);
            }

            //To substract from the unit price the included taxes mapped by the fiscal position
            this.fix_tax_included_price(line);

            if(options.discount !== undefined){
                line.set_discount(options.discount);
            }

            if(options.extras !== undefined){
                for (var prop in options.extras) {
                    line[prop] = options.extras[prop];
                }
            }

            var last_orderline = this.get_last_orderline();
            if( last_orderline && last_orderline.can_be_merged_with(line) && options.merge !== false){
                last_orderline.merge(line);
            }else{
                this.orderlines.add(line);
            }
            this.select_orderline(this.get_last_orderline());

            if(line.has_product_lot){
                this.display_lot_popup();
            }
        }
    });

    var _pos_model_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        scan_product: function(parsed_code){
            if (parsed_code.type === 'epc') {
                var selectedOrder = this.get_order();
                var product = this.db.get_product_by_barcode(parsed_code.base_code);

                if(!product){
                    return false;
                }

                selectedOrder.add_product_epc(product, {epc: parsed_code.value});
            }else{
                _pos_model_super.scan_product.apply(this, arguments);
            }
        },
    });

});
