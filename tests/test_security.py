from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from voting.models import Poll, Option


class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser('admin', 'a@b.com', 'apw')

    def test_sql_injection_search(self):
        # create polls
        Poll.objects.create(title="safe1")
        Poll.objects.create(title="safe2")
        # attempt SQL-like payload in search
        resp = self.client.get('/?q=' + "' OR 1=1 -- ")
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        # should return page without error; search input should be escaped in the HTML
        self.assertIn('Опросов не найдено.', content)
        self.assertIn('&#x27; OR 1=1 -- ', content)

    def test_xss_escaped_in_templates(self):
        p = Poll.objects.create(title='<script>alert(1)</script>')
        o = Option.objects.create(poll=p, text='opt')
        resp = self.client.get(f'/polls/{p.id}/')
        # raw <script> should not be present in response (it must be escaped)
        self.assertNotIn('<script>', resp.content.decode())

    def test_passwords_are_hashed(self):
        u = get_user_model().objects.create_user('u1', password='secret123')
        self.assertNotEqual(u.password, 'secret123')
        self.assertTrue(u.password.startswith('pbkdf2_') or u.password.count('$') >= 2)
