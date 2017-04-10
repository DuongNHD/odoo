from openerp.tests import common
from ..models.fonality import FonalityFailToCall
import requests


class TestFonalityModel(common.SingleTransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestFonalityModel, cls).setUpClass()
        user_model = cls.env['res.users']

        cls.user = user_model.create({
            'login': 'a_user',
            'password': 'pass',
            'name': 'a_user',
            'fonality_username': 'user',
            'fonality_password': 'pass',
            })
        cls.user._get_token = lambda: 'abcd'

    def setUp(self):
        self.user.write({'fonality_token': ''})

        def mock_call(number):
            mock_resp = requests.Response()
            mock_resp.status_code = 200
            return True, mock_resp
        self.user._call_fonality = mock_call

    def test_has_fonality_fields(self):
        for attr in ['fonality_username', 'fonality_password', 'fonality_token']:
            self.assertTrue(
                hasattr(self.user, attr),
                'No attribute {}'.format(attr))

    def test_refresh_fonality_token(self):
        self.user.refresh_fonality_token()
        self.assertEqual(self.user.fonality_token, 'abcd')

    def test_call_fonality(self):
        result = self.user.call_fonality('0123456789')
        self.assertTrue(result)

        result = self.user.call_fonality('0123456789', silent=True)
        self.assertIsInstance(result, tuple)

    def test_call_fonality_when_fail(self):
        def mock_call_raise(number):
            mock_resp = requests.Response()
            mock_resp.status_code = 200
            return False, mock_resp

        self.user._call_fonality = mock_call_raise

        result = self.user.call_fonality('0123456789', silent=True)
        self.assertIsInstance(result, tuple)
        self.assertFalse(result[0])

        with self.assertRaises(FonalityFailToCall) as ve:
            result = self.user.call_fonality('0123456789')
