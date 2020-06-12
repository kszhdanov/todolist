from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    title = models.CharField(max_length=250)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    text = models.CharField(max_length=250)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"'{self.text}' of organization '{self.organization.title}'"

    def short_desc(self):
        return self.text[:10] if len(self.text) > 10 else self.text
