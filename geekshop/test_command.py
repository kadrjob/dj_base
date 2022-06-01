from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class LoadDataTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('load_models_data_from_file','fixtures_data.json')
        self.assertIn('Expected output', out.getvalue())