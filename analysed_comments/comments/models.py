from django.db import models


class Comment(models.Model):
    STATUS_PENDING = 1
    STATUS_ANALYSED = 2
    STATUS_FAILED = 3
    _STATUSES = (
        (STATUS_PENDING, 'Pending Analysis'),
        (STATUS_ANALYSED, 'Analysis Complete'),
        (STATUS_FAILED, 'Analysis Failed'),
    )
    text = models.TextField(null=False, blank=False)
    status = models.PositiveIntegerField(
        choices=_STATUSES,
        default=STATUS_PENDING
    )
    is_positive = models.NullBooleanField()
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text
