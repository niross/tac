from django.db.models.signals import post_save
from django.dispatch import receiver

from comments.models import Comment
from comments.tasks import analyse_comment


@receiver(post_save, sender=Comment)
def comment_save(sender, instance, created, **kwargs):
    """
    Comment post save handler.

    Queue an analysis task when a comment is saved.

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if (instance.status == instance.STATUS_PENDING) and not kwargs['raw']:
        analyse_comment.delay(instance.id)
