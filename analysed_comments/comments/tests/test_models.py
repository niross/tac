from django.test import TestCase

import mock

from analysed_comments.comments.models import Comment


class CommentTest(TestCase):
    def create_comment(self, text="This is a comment"):
        return Comment.objects.create(text=text)

    @mock.patch('analysed_comments.comments.tasks.analyse_comment.delay')
    def test_comment_creation(self, analyse_task):
        comment = self.create_comment()
        self.assertTrue(isinstance(comment, Comment))
        self.assertTrue(comment.__unicode__(), comment.text)
        self.assertTrue(analyse_task.called_once_with(comment.id))

    @mock.patch('analysed_comments.comments.tasks.analyse_comment.delay')
    def test_comment_update(self, analyse_task):
        comment = self.create_comment()
        comment.text = 'An updated comment'
        comment.save()
        self.assertTrue(analyse_task.called_once_with(comment.id))
