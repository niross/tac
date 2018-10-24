from rest_framework import serializers

from analysed_comments.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    is_positive = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'status', 'text', 'is_positive', 'created', 'updated')

    @staticmethod
    def get_status(instance):
        return {
            'id': instance.status,
            'name': instance.get_status_display()
        }
