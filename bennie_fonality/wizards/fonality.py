# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import except_orm

import requests

import logging
logger = logging.getLogger(__name__)


class FonalityConfig(models.TransientModel):
    _name = 'fonality.config'
    url = fields.Char(
            required=True,
            default=lambda self: \
            self.env['ir.config_parameter'].get_param('fonality.api_url')
            ) 

    @api.multi
    def configure(self): 
        self.env['ir.config_parameter'].set_param('fonality.api_url', self.url)
        return True


class FonalityTestCall(models.TransientModel):
    _name = 'fonality.test_call'
    number = fields.Char()
    response_text = fields.Char()

    @api.multi
    def call(self): 
        login_user = self.env['res.users'].browse(self.env.uid)
        try:
            successful, result = login_user.call_fonality(
                    self.number,
                    silent=True)
        except Exception as e:
            logger.error("Fail to test call", exc_info = e)
            successful = False
            result = 'Fail to call because: {}'.format(str(e))
 
        self.write({
            'number': '',
            'response_text': result
            })

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        } 
