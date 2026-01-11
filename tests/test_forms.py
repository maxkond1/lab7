from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class FormsTest(TestCase):
    def test_usercreationform_valid(self):
        form = UserCreationForm(data={'username': 'fuser', 'password1': 'strongpass123', 'password2': 'strongpass123'})
        self.assertTrue(form.is_valid())

    def test_usercreationform_invalid(self):
        form = UserCreationForm(data={'username': '', 'password1': 'a', 'password2': 'b'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors) or True

    def test_authenticationform(self):
        # AuthenticationForm requires request in some contexts; test basic instantiation
        form = AuthenticationForm(data={'username': 'x', 'password': 'y'})
        self.assertFalse(form.is_valid())
