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

    def test_export_invalid_fields(self):
        self.client.login(username='admin', password='adminpass')
        resp = self.client.get('/admin/export-xlsx/?table=poll&fields=title,nonexistent')
        self.assertEqual(resp.status_code, 400)


class GuestVoteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.poll = Poll.objects.create(title='G Poll')
        self.opt = Option.objects.create(poll=self.poll, text='Opt')

    def test_guest_cannot_vote_twice_from_same_ip(self):
        url = f'/polls/{self.poll.id}/'
        # first vote should succeed
        resp1 = self.client.post(url, {'option': self.opt.id}, REMOTE_ADDR='127.0.0.1')
        self.assertIn(resp1.status_code, (302, 301))
        # second vote from same IP should be forbidden
        resp2 = self.client.post(url, {'option': self.opt.id}, REMOTE_ADDR='127.0.0.1')
        self.assertEqual(resp2.status_code, 403)
