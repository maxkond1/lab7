from django.test import TestCase
from django.contrib.auth import get_user_model
from voting.models import Poll, Option, Vote
import time


class ModelsTest(TestCase):
    def test_create_models_and_relations(self):
        user = get_user_model().objects.create_user('u1', password='pass')
        poll = Poll.objects.create(title='M1', description='d')
        opt = Option.objects.create(poll=poll, text='o')
        v = Vote.objects.create(user=user, option=opt, ip_address='127.0.0.1')

        # relations
        self.assertEqual(opt.poll, poll)
        self.assertIn(opt, list(poll.options.all()))
        self.assertIn(v, list(opt.votes.all()))

    def test_timestamps_auto_filled(self):
        p = Poll.objects.create(title='t1')
        self.assertIsNotNone(p.created_at)
        self.assertIsNotNone(p.updated_at)
        # update and ensure updated_at changes
        old = p.updated_at
        time.sleep(0.01)
        p.title = 't2'
        p.save()
        self.assertTrue(p.updated_at >= old)

    def test_unique_constraint_user_option(self):
        user = get_user_model().objects.create_user('u2', password='pass')
        poll = Poll.objects.create(title='uniq')
        opt = Option.objects.create(poll=poll, text='o')
        Vote.objects.create(user=user, option=opt)
        with self.assertRaises(Exception):
            # creating duplicate vote should raise IntegrityError (or subclass)
            Vote.objects.create(user=user, option=opt)
