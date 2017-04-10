# -*- coding: utf-8 -*-

from openerp import models, fields, api


class MakeCallWizard(models.TransientModel):
    _name = 'x.make_call'

    def _default_applicant(self):
        return self.env['res.partner'].browse(
                self._context.get('active_id')
                )

    partner_id = fields.Many2one(
            'res.partner',
            string='Applicant',
            required=True,
            default=_default_applicant,
            ondelete="cascade",
            )
    next_call = fields.Datetime("Next Call")
    
    @api.multi
    def save_make_call(self):
        return self.partner_id.set_make_call(self.next_call)
