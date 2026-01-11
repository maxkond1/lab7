from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    """Abstract base model that provides timestamps for all inheriting models.

    Fields:
    - created_at: timestamp when record was created
    - updated_at: timestamp when record was last updated
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Poll(BaseModel):
    """A poll that contains several options to vote for."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Option(BaseModel):
    """Option belonging to a `Poll`. Users vote for an `Option`."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.poll.title} - {self.text}"


class Vote(BaseModel):
    """Vote for a specific `Option`.

    The `user` field may be null for guest votes. `unique_together` is
    used to prevent duplicate votes by the same user for the same option.
    """
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes')
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'option')

    def __str__(self):
        return f"Vote by {self.user} on {self.option}"
