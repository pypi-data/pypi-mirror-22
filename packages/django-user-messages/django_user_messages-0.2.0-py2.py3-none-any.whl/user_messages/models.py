from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    created_at = models.DateTimeField(
        _('created at'),
        default=timezone.now,
    )
    delivered_at = models.DateTimeField(
        _('delivered at'),
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='+',
    )
    message = JSONField(
        _('message'),
        default=dict,
    )
    deliver_once = models.BooleanField(
        _('deliver once'),
        default=True,
    )

    meta = JSONField(
        _('meta data'),
        default=dict,
        blank=True,
        help_text=_(
            'Additional data with user-/developer-defined significance.'
        ),
    )

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    # Duck typing django.contrib.messages.storage.base.Message
    def __str__(self):
        return self.message['message']

    @property
    def tags(self):
        return ' '.join(tag for tag in [
            self.message['extra_tags'],
            self.level_tag,
        ] if tag)

    @property
    def level_tag(self):
        from django.contrib.messages.storage.base import LEVEL_TAGS

        return LEVEL_TAGS.get(self.message['level'], '')
