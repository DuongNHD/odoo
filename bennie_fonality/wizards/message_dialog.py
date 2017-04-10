from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class FonalityMessageDialogWizard(models.TransientModel):
    _name = 'fonality.message_dialog'

    message = fields.Char(default=lambda self: self._get_default_message())

    @api.multi
    def perform_ok(self):
        return {}

    @api.multi
    def _get_default_message(self):
        return self._context.get('message')

    @api.multi
    def show_dialog(self, title, message, src_model="res.partner"):
        return {
            "type": "ir.actions.act_window",
            "name": title,
            "target" : "new",
            "src_model": src_model,
            "res_model": "fonality.message_dialog",
            "view_mode": "form",
            "view_type": "form",
            "context": {
                "message": message
            },
        }
