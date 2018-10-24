from django.db.models.signals import post_save
from django.dispatch import receiver

from analysed_comments.comments.models import Comment
from analysed_comments.comments.tasks import analyse_comment


@receiver(post_save, sender=Comment)
def comment_save(sender, instance, **kwargs):
    """
    Comment post save handler.

    Queue an analysis task when a comment is saved.

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if (instance.status == instance.STATUS_PENDING) and not kwargs['raw']:
        analyse_comment.delay(instance.id)


