# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import except_orm, ValidationError
from simplejson import JSONDecodeError

import requests

import logging
logger = logging.getLogger(__name__)


class FonalityFailToCall(Exception):
    pass


class FonalityPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    fonality_username    = fields.Char()
    fonality_password    = fields.Char()
    fonality_token       = fields.Char()


class FonalityUser(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    @api.multi
    def refresh_fonality_token(self):
        try:
            self._refresh_fonality_token()
        except FonalityFailToCall as fe:
            raise ValidationError(str(fe))

    @api.multi
    def clear_fonality_token(self):
        self.write({'fonality_token': ''})

    @api.multi
    def call_fonality(self, number, silent=False):
        if not self.fonality_token:
            self._refresh_fonality_token()

        if not number:
            error_text = 'Number is required'
            if silent:
                return False, 'Number is required'
            
            raise FonalityFailToCall(error_text)
            
        successful, resp = self._call_fonality(number)
        if silent:
            return successful, resp.content

        if not successful:
            raise FonalityFailToCall

        return True

    @api.multi
    def write(self, vals):
        if 'fonality_username' in vals or 'fonality_password' in vals:
            vals['fonality_token'] = ''

        return super(FonalityUser, self).write(vals)

    def _refresh_fonality_token(self):
        token = self._get_token()
        self.write({'fonality_token': token})

    def _get_fonality_api_url(self):
        config_model = self.env['ir.config_parameter']
        return config_model.get_param('fonality.api_url')

    def _get_token(self):
        api_url = self._get_fonality_api_url()
        headers  = {'Access-Control-Allow-Credentials': True, 'X-Requested-By': 'FonalityClickToDial'}
        post_data = {
            'method' : 'login',
            'user'   : self.fonality_username,
            'pass'   : self.fonality_password
        }
        logger.debug("request url : {}".format(api_url))

        try:
            resp = requests.post(api_url, data=post_data, headers=headers)
            resp_dict = resp.json()
            logger.debug("response : {}".format(resp.content))
            return resp_dict['token']
        except KeyError:
            logger.error("Fail to connect to fonality : KeyError")
            raise FonalityFailToCall("Authentication Error")
        except JSONDecodeError:
            logger.error("Fail to connect to fonality : JSONDecodeError")
            raise FonalityFailToCall(
                "Wrong Response format. You may need to check API url."
                )
        except:
            logger.error("Fail to connect to fonality")
            raise

    def _call_fonality(self, number):
        api_url = self._get_fonality_api_url()
        params = {
            'method'     : 'dial',
            'number'     : number,
            'dontmodify' : 1,
            'token'      : self.fonality_token
        }
        resp = requests.get(api_url, params=params)
        resp_dict = resp.json()

        return 'result' in resp_dict and resp_dict['result'] == 'Success', resp
        
