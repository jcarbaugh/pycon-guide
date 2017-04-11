import uuid

import pytz
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


pacific = pytz.timezone('America/Los_Angeles')


def this_year():
    return timezone.now().year


def uuid_hex():
    return uuid.uuid4().hex


class Calendar(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='calendar')
    slug = models.CharField(_('Slug'), max_length=32, default=uuid_hex)

    def __str__(self):
        return self.slug


class PyCon(models.Model):
    year = models.PositiveSmallIntegerField(
        _('Year'), default=this_year, unique=True)
    location = models.CharField(
        _('Location'), max_length=128,
        help_text=_('The locality and region where the conference is held'))

    class Meta:
        ordering = ('-year',)
        verbose_name = 'PyCon'
        verbose_name_plural = 'PyCons'

    def __str__(self):
        return 'PyCon {} {}'.format(self.year, self.location)


class Presentation(models.Model):
    pycon = models.ForeignKey(PyCon, related_name='presentations')
    presentation_id = models.PositiveSmallIntegerField(_('PyCon ID'))
    title = models.CharField(_('Title'), max_length=255)
    url = models.URLField(_('URL'), blank=True)
    category = models.CharField(_('Category'), max_length=128, blank=True)
    audience = models.CharField(_('Audience'), max_length=64, blank=True)
    speakers = models.TextField(_('Speakers'), blank=True)
    abstract = models.TextField(_('Abstract'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    start_time = models.DateTimeField(_('Start Time'))
    end_time = models.DateTimeField(_('End Time'))
    room = models.CharField(_('Room'), max_length=64, blank=True)
    duration_minutes = models.PositiveSmallIntegerField(
        _('Duration'), blank=True, null=True,
        help_text=_('Presentation duration in minutes'))

    class Meta:
        ordering = ('start_time', 'end_time', 'title')
        unique_together = ('pycon', 'presentation_id')

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        td = self.end_time - self.start_time
        self.duration_minutes = abs(td.seconds) / 60
        super(Presentation, self).save(**kwargs)

    @property
    def local_start_time(self):
        return self.start_time.astimezone(pacific)

    @property
    def local_end_time(self):
        return self.end_time.astimezone(pacific)


class Interest(models.Model):
    user = models.ForeignKey(User, related_name='interests')
    presentation = models.ForeignKey(Presentation, related_name='interests')

    def __str__(self):
        return '{} in {}'.format(self.user, self.presentation)
