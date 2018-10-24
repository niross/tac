from celery.task import task

from comments.models import Comment


@task
def analyse_comment(comment_id):
    """
    TODO: Document properly

    :param comment_id:
    :return:
    """
    comment = Comment.objects.get(id=comment_id)
    print('TODO')