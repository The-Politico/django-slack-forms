from django.db import models


class Test(models.Model):
    """
    A test model.
    """

    age = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    permissions = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
