from rest_framework import viewsets

from analysed_comments.comments.models import Comment
from analysed_comments.comments.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    test

    retrieve:
    Return the given comment.

    list:
    Return a list of all non-deleted comments.

    create:
    Create a new comment.

    update:
    Update an existing comment.
    """
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_update(self, serializer):
        """
        When a comment is updated set the status to pending and it will be re-analysed.
        :param serializer:
        :return:
        """
        instance = serializer.save()
        instance.state = Comment.STATUS_PENDING
        instance.save()
