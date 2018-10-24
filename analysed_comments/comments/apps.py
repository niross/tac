from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'comments'

    def ready(self):
        super().ready()
        from . import signals  # noqa
