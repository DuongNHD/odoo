# -*- coding: utf-8 -*-
from openerp import api, fields, models, tools, _
from datetime import datetime, timedelta
import re


class CallHistory(models.Model):
    _name = 'x.call_history'

    user = fields.Many2one('res.users', 'User call')
    mobile = fields.Char('Mobile No')
    call_date = fields.Datetime('Call Date')


class MakeCallPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def set_num_call(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Make Call",
            "target": "new",
            "src_model": "res.partner",
            "res_model": "x.make_call",
            "view_mode": "form",
            "view_type": "form",
            "context": {
                "active_id": self.id,
            },
        }

    @api.multi
    def make_call(self):
        user = self.env['res.users'].browse([self.env.uid])

        user.call_fonality(re.sub('\D', '', self.mobile), silent=False)
        call_history = self.env['x.call_history']
        data = {}
        data.update({
            'user': self.uid,
            'mobile': self.mobile,
            'call_date': fields.datetime.now(),
        })
        call_history.create(data)
        self.message_post(cr=self.env.cr,
                          uid=self.env.uid,
                          body="Making call to %s" % self.mobile_mask)
        return self.env['fonality.message_dialog'].show_dialog(
            'Call Placed.',
            'Softphone will appear soon.'
        )

    @api.multi
    def set_make_call(self, next_call):
        self.write({'num_call': self.num_call + 1,
                    'last_call': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'next_call': next_call})