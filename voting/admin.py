from django.contrib import admin
from .models import Poll, Option, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll', 'created_at')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'ip_address', 'created_at')
