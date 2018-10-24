from rest_framework import viewsets

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, editing and deleting Comments
    """
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        """
        When a comment is updated set the status to pending and it will be re-analysed.
        :param serializer:
        :return:
        """
        serializer.instance.state = Comment.STATUS_PENDING
        serializer.save()
