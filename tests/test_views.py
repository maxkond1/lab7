from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from voting.models import Poll, Option, Vote


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user('uview', password='pw')
        self.admin = get_user_model().objects.create_superuser('admin', 'a@b.com', 'apw')
        self.poll = Poll.objects.create(title='VPoll')
        self.opt = Option.objects.create(poll=self.poll, text='opt')

    def test_public_urls(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(f'/polls/{self.poll.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_admin_export_access(self):
        # anon should be redirected
        resp = self.client.get('/admin/export-xlsx/')
        self.assertIn(resp.status_code, (302, 301))
        # login as admin
        self.client.login(username='admin', password='apw')
        resp = self.client.get('/admin/export-xlsx/')
        self.assertEqual(resp.status_code, 200)

    def test_vote_flow_authenticated(self):
        self.client.login(username='uview', password='pw')
        url = f'/polls/{self.poll.id}/'
        resp = self.client.post(url, {'option': self.opt.id})
        # should redirect back to poll detail
        self.assertIn(resp.status_code, (302, 301))
        self.assertEqual(Vote.objects.filter(user=self.user).count(), 1)

    def test_guest_cannot_access_admin(self):
        resp = self.client.get('/admin/')
        self.assertIn(resp.status_code, (302, 301))
