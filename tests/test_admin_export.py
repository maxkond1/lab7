from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from voting.models import Poll
import io
import openpyxl


class AdminExportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser('admin', 'a@b.com', 'apw')
        Poll.objects.create(title='E1', description='d1')

    def test_export_xlsx_file_structure(self):
        self.client.login(username='admin', password='apw')
        resp = self.client.get('/admin/export-xlsx/?action=download&table=poll&fields=title,description')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', resp['Content-Type'])
        data = io.BytesIO(resp.content)
        wb = openpyxl.load_workbook(data)
        ws = wb.active
        # header row equals requested fields
        headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        self.assertEqual(headers, ['title', 'description'])
