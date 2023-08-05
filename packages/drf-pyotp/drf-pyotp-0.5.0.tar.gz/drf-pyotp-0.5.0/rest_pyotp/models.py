#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- rest_pyotp.models
~~~~~~~~~~~~~~

- This file holds the necessary models for pyotp service
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local


# own app


class PyOTP(models.Model):
    """pyotp model

        Here we will store secret of every generated otp. So that on verification of OTP we know which secret to use
    """

    # Attributes
    uuid = models.UUIDField(
            _('OTP Unique uuid'),
            unique=True,
            default=uuid.uuid4,
            editable=False,
            help_text=_('Non-editable, to be generated by system itself.'),
    )
    secret = models.CharField(
            _('Secret'),
            null=False,
            blank=False,
            max_length=50,
            help_text=_('Secret used to generate OTP.'),
    )
    count = models.IntegerField(
            _('Count'),
            null=True,
            blank=True,
            help_text=_('OTP Count, to be used in case of HOTP.'),
    )
    interval = models.IntegerField(
            _('Interval (in seconds)'),
            null=True,
            blank=True,
            help_text=_('OTP Count, to be used in case of TOTP.'),
    )
    otp = models.CharField(
            _('OTP'),
            null=False,
            blank=False,
            max_length=10,
            help_text=_('Generated OTP.'),
    )
    name = models.CharField(
            _('Account Name'),
            null=True,
            blank=True,
            max_length=255,
            help_text=_('Account Name for Provisioning URI, to be used when need URI for QR code.'),
    )
    initial_count = models.IntegerField(
            _('Initial Count'),
            null=True,
            blank=True,
            help_text=_('Initial Count for Provisioning URI.'),
    )
    issuer_name = models.CharField(
            _('Issuer Name'),
            null=True,
            blank=True,
            max_length=255,
            help_text=_('Issuer Name for Provisioning URI.'),
    )
    created_at = models.DateTimeField(
                 _('created at'),
                 auto_now_add=True,
                 db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("PyOtp")
        verbose_name_plural = _("PyOtp")

    # Functions
    def __str__(self):
        return str(self.uuid)
