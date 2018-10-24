import mock
from django.urls import reverse

import factory
import factory.fuzzy
from rest_framework import status
from rest_framework.test import APITestCase

from comments.models import Comment


class CommentFactory(factory.DjangoModelFactory):
    text = factory.fuzzy.FuzzyText()

    class Meta:
        model = Comment


class CommentAPITestCase(APITestCase):
    @mock.patch('comments.tasks.analyse_comment.delay')
    def test_list_comments(self, analyse_task):
        CommentFactory()
        CommentFactory()
        response = self.client.get(
            reverse('comments-api:comment-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_post_comment_invalid(self):
        response = self.client.post(
            reverse('comments-api:comment-list'),
            data={
                'text': ''
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'text': ['This field may not be blank.']})

    @mock.patch('comments.tasks.analyse_comment.delay')
    def test_post_comment(self, analyse_task):
        response = self.client.post(
            reverse('comments-api:comment-list'),
            data={
                'text': 'A test comment'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(pk=response.json()['id'])
        self.assertEqual(comment.text, 'A test comment')
        self.assertEqual(comment.status, Comment.STATUS_PENDING)
        self.assertTrue(analyse_task.called_once_with(comment.id))

    @mock.patch('comments.tasks.analyse_comment.delay')
    def test_put_comment_invalid(self, analyse_task):
        comment = CommentFactory()
        response = self.client.put(
            reverse('comments-api:comment-detail', args=(comment.id,)),
            data={
                'text': ''
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'text': ['This field may not be blank.']})

    @mock.patch('comments.tasks.analyse_comment.delay')
    def test_put_comment(self, analyse_task):
        comment = CommentFactory()
        response = self.client.put(
            reverse('comments-api:comment-detail', args=(comment.id,)),
            data={
                'text': 'An updated comment'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment = Comment.objects.get(pk=comment.id)
        self.assertEqual(comment.text, 'An updated comment')
        self.assertEqual(comment.status, Comment.STATUS_PENDING)
        self.assertEqual(analyse_task.call_count, 2)

    def test_get_non_existent_comment(self):
        response = self.client.get(reverse('comments-api:comment-detail', args=(999,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch('comments.tasks.analyse_comment.delay')
    def test_get_deleted_comment(self, analyse_task):
        comment = CommentFactory()
        comment.deleted = True
        comment.save()
        response = self.client.get(reverse('comments-api:comment-detail', args=(comment.id,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch('comments.tasks.analyse_comment.delay')
    def test_get_comment(self, analyse_task):
        comment = CommentFactory()
        response = self.client.get(reverse('comments-api:comment-detail', args=(comment.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], comment.id)

    def test_delete_non_existent_comment(self):
        response = self.client.delete(reverse('comments-api:comment-detail', args=(999,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch('comments.tasks.analyse_comment.delay')
    def test_delete_comment(self, analyse_task):
        comment = CommentFactory()
        response = self.client.delete(reverse('comments-api:comment-detail', args=(comment.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
