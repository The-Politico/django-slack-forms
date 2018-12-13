import uuid

from django.db import models


class Token(models.Model):
    """
    A registered token for endpoint validation.
    """

    name = models.SlugField(
        max_length=100, unique=True, help_text="The name of your token."
    )
    token = models.SlugField(max_length=30, unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex[:30]
        super().save(*args, **kwargs)
