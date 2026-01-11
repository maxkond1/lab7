from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from voting.models import Poll, Option


class Command(BaseCommand):
    help = 'Create demo users and polls'

    def handle(self, *args, **options):
        User = get_user_model()
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_pass = 'Secur3Pass!'
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(admin_username, admin_email, admin_pass)
            self.stdout.write(self.style.SUCCESS(f'Created superuser: {admin_username}/{admin_pass}'))
        else:
            self.stdout.write('Superuser already exists')

        user_username = 'user1'
        user_pass = 'pass1234'
        if not User.objects.filter(username=user_username).exists():
            User.objects.create_user(user_username, 'user1@example.com', user_pass)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user_username}/{user_pass}'))
        else:
            self.stdout.write('User user1 already exists')

        # Create sample polls
        samples = [
            ('Favorite color', 'Choose your favorite color', ['Red', 'Green', 'Blue']),
            ('Best programming language', 'Vote for the best language', ['Python', 'JavaScript', 'C++']),
        ]
        for title, desc, opts in samples:
            p, created = Poll.objects.get_or_create(title=title, defaults={'description': desc, 'is_active': True})
            if created:
                for o in opts:
                    Option.objects.create(poll=p, text=o)
                self.stdout.write(self.style.SUCCESS(f'Created poll: {title}'))
            else:
                self.stdout.write(f'Poll already exists: {title}')

        self.stdout.write(self.style.SUCCESS('Demo data creation complete'))
