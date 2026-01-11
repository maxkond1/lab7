from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Poll, Option, Vote


class VotingModelTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(title='Test Poll', description='Desc')
        self.opt1 = Option.objects.create(poll=self.poll, text='A')
        self.opt2 = Option.objects.create(poll=self.poll, text='B')
        self.user = get_user_model().objects.create_user(username='tester', password='pass')

    def test_vote_creation(self):
        vote = Vote.objects.create(user=self.user, option=self.opt1)
        self.assertEqual(self.opt1.votes.count(), 1)

    def test_guest_vote_allowed(self):
        vote = Vote.objects.create(user=None, option=self.opt2, ip_address='127.0.0.1')
        self.assertEqual(self.opt2.votes.count(), 1)


class AdminExportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser('admin', 'a@b.com', 'adminpass')

    def test_export_requires_login(self):
        resp = self.client.get('/admin/export-xlsx/')
        # redirect to login
        self.assertIn(resp.status_code, (302, 301))

    def test_export_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        resp = self.client.get('/admin/export-xlsx/?table=poll&fields=title,description')
        # successful download or rendered form
        self.assertIn(resp.status_code, (200, 302))
