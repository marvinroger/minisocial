"""Models"""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Message(models.Model):
    """This represents a Message."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.CharField(max_length=140)
    pub_date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.message_text

@python_2_unicode_compatible
class MessageHistory(models.Model):
    """
    This represents a Message History entry.
    This is useful to store messages additions and deletions.
    """

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_addition = models.BooleanField() # true if addition, false if deletion

    def __str__(self):
        return self.message_text
