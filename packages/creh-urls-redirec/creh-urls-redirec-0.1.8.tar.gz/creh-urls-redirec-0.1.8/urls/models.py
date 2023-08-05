# -*- coding: utf-8 -*-
from . import constants
from django.db import models
from django.utils import timezone


class UrlRedirect(models.Model):

    url_source = models.TextField(unique=True)

    url_destination = models.TextField()

    date_initial_validity = models.DateTimeField(
        default=timezone.now(),
    )

    date_end_validity = models.DateTimeField(
        default=timezone.now(),
    )

    views = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    is_active = models.SmallIntegerField(
        choices=constants.STATUS_CHOICES,
        default=constants.STATUS_TRUE
    )

    is_permanent = models.SmallIntegerField(
        choices=constants.STATUS_CHOICES,
        default=constants.STATUS_TRUE
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        default=timezone.now(),
        editable=False,
    )

    updated_at = models.DateTimeField(
        default=timezone.now(),
        editable=False,
    )

    def __str__(self):
        return "({}) {}".format(self.is_permanent, self.url_source)

from signals import post_save_url,post_delete_url