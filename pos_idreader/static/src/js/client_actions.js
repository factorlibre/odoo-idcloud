odoo.define('pos_idreader.client_actions', function(require){
    "use strict"
    var ajax = require('web.ajax');
    var core = require('web.core');
    var ControlPanelMixin = require('web.ControlPanelMixin');

    function SetOutputPower(parent, action) {
        var params = {"output_power": action.params.output_power, "region": action.params.region}

        var data = {
          id: action.context.active_id,
          jsonrpc: "2.0",
          method: "output",
          params: params || {}
        }
        jQuery.ajax({
          type: "POST",
          url: action.params.url,
          dataType: 'json',
          contentType: "application/json",
          async: true,
          crossDomain: true,
          data: JSON.stringify(data),
          success: function (response) {
            console.log(response);
          },
        });
    }
    core.action_registry.add('idreader.set_output_power', SetOutputPower);
});
