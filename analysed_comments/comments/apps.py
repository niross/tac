from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'analysed_comments.comments'

    def ready(self):
        super().ready()
        from . import signals  # noqa
