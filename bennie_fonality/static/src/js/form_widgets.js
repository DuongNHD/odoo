// path_to_your_module/static/src/js/form_widgets.js
odoo.define('fonality.form_widgets', function (require) {
    "use strict";

    var core = require('web.core');
    var form_common = require('web.form_common');
    var FieldChar = core.form_widget_registry.get('char');
    // this is widget for unique CharField
    var FonalityPhoneText = FieldChar.extend({
        template: 'FonalityPhoneText',
        events: {
            'click button.btn_click2call': function(e) {
                var value = this.get('value')?this.get('value').replace(/\D/g, ''):null;
                var self = this;
                var log_message = this.options.log_message || "Making call {}"
                var button = $(e.currentTarget);

                button.attr('disabled', 'disabled');

                var current_url = location.href;
                var current_model = current_url.match(/model=([^\&]+)/m);
                var current_id = current_url.match(/id=([^\&]+)/m);

                if(value) {
                    var fonality = new openerp.web.Model("fonality.calling_dialog");

                    var context = new openerp.web.CompoundContext({
                        'calling_log_model': current_model?current_model[1]:false,
                        'calling_log_model_id': current_id?current_id[1]:false,
                        'calling_log_message': log_message
                    });

                    fonality.call("call", {context: context, number: value}).then(function(result) {
                       console.log(result);
                       button.removeAttr('disabled');
                       self.do_action({
                            type: 'ir.actions.act_window',
                            res_model: "fonality.message_dialog",
                            views: [[false, 'form']],
                            target: 'new',
                            context: {
                                message: 'Call Placed'
                            }
                        });
                    });
                } else {
                    button.removeAttr('disabled');
                    self.do_action({
                         type: 'ir.actions.act_window',
                         res_model: "fonality.message_dialog",
                         views: [[false, 'form']],
                         target: 'new',
                         context: {
                             message: 'No number specified.'
                         }
                     });
                }
            }
        },
        start: function() {
            console.log("start");

            return this._super();
        },
        render_value: function() {
            this._super();

            var self = this;
            var value = this.get('value')?this.get('value').replace(/\D/g, ''):null;
            var users = new openerp.web.Model('res.users');

            self.$('button').removeAttr('disabled');

            if(self.get('effective_readonly')) {
                if(!value) {
                    self.$('button').css({
                        visibility: 'hidden'
                    });
                } else {
                    users.call('has_group', ['fonality.group_callable']).done(function(is_inrole) {
                        if (!is_inrole) {
                            self.$('button').replaceWith('<span class="oe_form_char_content"></span>');
                        }

                        users.call('has_group', ['fonality.group_supervisor']).done(function(is_inrole) {
                            if (is_inrole) {
                                self.$('.oe_form_char_content').text(value);
                            } else {
                                self.$('.oe_form_char_content').text(value.substring(0,2) + 'xxxx' + value.substring(value.length - 4));
                            }
                        });
                    });
                }
            } else {
                users.call('has_group', ['fonality.group_supervisor']).done(function(is_inrole) {
                    if (is_inrole) {
                        self.$('input').val(value);
                    } else {
                        if(value) {
                            self.$('input').replaceWith('<span>' + value.substring(0,2) + 'xxxx' + value.substring(value.length - 4) + '</span>');
                        } else {
                            self.$('input').replaceWith('<span>not specified</span>');
                        }
                    }
                })
            }
        }
    });
    // register unique widget, because Odoo does not know anything about it
    core.form_widget_registry.add('fonality', FonalityPhoneText);

});
