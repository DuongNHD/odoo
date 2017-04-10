from openerp import models, fields, api, _
from openerp.http import request
import re
import logging

_logger = logging.getLogger(__name__)


class FonalityCallingDialog(models.TransientModel):
    _name = 'fonality.calling_dialog'

    @api.model
    def call(self, number):
        user = self.env['res.users'].browse([self.env.uid])

        user.call_fonality(re.sub('\D', '', number), silent=False)

        _logger.debug(number)
        _logger.debug("Active Model: %s" % self._context.get('calling_log_model'))
        _logger.debug("Active ID: %s" % self._context.get('calling_log_model_id'))

        try:
            active_model = self._context.get('calling_log_model')
            active_id = int(self._context.get('calling_log_model_id'))
            log_message = self._context.get('calling_log_message', 'Making call {}')
            log_message = log_message.format("{}xxxx{}".format(number[0:2], number[-4:]))

            model = self.env[active_model].browse(active_id)
            model.message_post(cr=self.env.cr,
                               uid=self.env.uid,
                               body=log_message)

        except Exception as ex:
            _logger.error("Something went wrong", exc_info=ex)

        return self.env['fonality.message_dialog'].show_dialog(
            'Call Placed.',
            'Softphone will appear soon.'
        )
