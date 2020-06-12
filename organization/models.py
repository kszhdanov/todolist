import binascii
import os

from django.contrib import auth
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organization(models.Model):
    title = models.CharField(max_length=250)
    users = models.ManyToManyField(auth.get_user_model())

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    text = models.CharField(max_length=250)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"'{self.text}' of organization '{self.organization.title}'"

    def short_desc(self):
        return self.text[:10] if len(self.text) > 10 else self.text


class CustomToken(models.Model):
    key = models.CharField(_("Key"), max_length=40)
    user = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("CustomToken")
        verbose_name_plural = _("CustomTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f"Token '{self.key}', organization '{self.organization.title}', user '{self.user}'"
