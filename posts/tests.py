from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# Create your tests here.
from .models import Post, Tag


def create_post(title, author, is_draft=True):
    return Post.objects.create(title=title, author=author, is_draft=is_draft)


class TagModelTests(TestCase):

    def test_colored_code(self):
        """
        method should return a html <span> element containing the tags
        color_code
        """
        tag = Tag(name='ruby', color_code='#cc342d')
        self.assertEqual(
            tag.colored_code(), '<span style="color: #cc342d;"> #cc342d</span>'
        )

    def test_get_absolute_url(self):
        tag = Tag.objects.create(name='programming')
        self.assertEqual(
            reverse('posts:tag_detail', args=[tag.slug]), tag.get_absolute_url()
        )

    def test_str(self):
        self.assertEqual(str(Tag(name='ruby')), 'ruby')


class PostModelManagersTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='homer', email='homer@simpson', password='secret'
        )
        create_post('draft', self.user, is_draft=True)
        create_post('test', self.user, is_draft=False)

    def test_draft_model_manager(self):
        """
        the draft model manager should only return draft posts
        """
        self.assertQuerysetEqual(Post.drafts.all(), ['<Post: draft>'])

    def test_published_model_manager(self):
        """
        the published model manager should only return published posts
        """
        self.assertQuerysetEqual(Post.published.all(), ['<Post: test>'])


class PostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='homer', email='homer@simpson', password='secret'
        )

    def test_get_absolute_url(self):
        post = create_post('hello world', self.user)
        self.assertEqual(
            reverse('posts:post_detail', args=[post.slug]),
            post.get_absolute_url(),
        )

    def test_str(self):
        self.assertEqual(str(Post(title='test')), 'test')


class HideUnpublishedPostsForAnonymousUsersTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='jesus', email='jesus@nazareth', password='secret'
        )
        self.post = create_post('test', author=self.admin, is_draft=False)
        self.draft = create_post('draft', author=self.admin, is_draft=True)

    def test_archive_hides_draft_posts(self):
        now = timezone.now()
        response = self.client.get(
            reverse('posts:archive_month', args=[now.year, now.month])
        )
        self.assertQuerysetEqual(response.context['posts'], ['<Post: test>'])

    def test_search_hides_unpublished_posts(self):
        """
        the search view should only return results from published posts
        """
        response = self.client.get(reverse('posts:post_search') + '?q=draft')
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_draft_post_route_404s(self):
        """
        anonymous users should be greeted by a 404 page attemping to access
        the URL matching a post that is unpublished
        """
        slug = self.draft.slug
        response = self.client.get(reverse('posts:post_detail', args=[slug]))
        self.assertEqual(response.status_code, 404)

    def test_unpublished_posts_are_hidden(self):
        """
        unpublished posts should be hidden to anonymous users
        """
        response = self.client.get(reverse('posts:index'))
        self.assertQuerysetEqual(response.context['posts'], ['<Post: test>'])

    def test_unpublished_posts_visible_to_admin(self):
        """
        unpublished ('draft') posts should be only be visible to superusers
        """
        self.client.login(username=self.admin.username, password='secret')
        response = self.client.get(reverse('posts:index'))
        self.assertQuerysetEqual(
            response.context['posts'], ['<Post: draft>', '<Post: test>']
        )


class TestPublishPost(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='jesus', email='jesus@nazareth', password='secret'
        )

    def test_publish_post(self):
        """
        A post request from an authenticated user to the post_publish endpoint
        should set a posts published field to True
        """
        post = create_post('draft', self.admin, is_draft=True)
        self.client.login(username=self.admin.username, password='secret')
        response = self.client.post(
            reverse('posts:post_publish', args=[post.pk]), follow=True
        )
        self.assertRedirects(response, post.get_absolute_url())
        self.assertFalse(response.context['post'].is_draft)

    def test_prevent_wrong_author_publishing_post(self):
        post = create_post('draft', self.admin)
        self.user = User.objects.create_user(
            username='Homer', email='homer@simpson', password='secret'
        )
        self.client.login(username=self.user.username, password='secret')
        response = self.client.post(
            reverse('posts:post_publish', args=[post.pk]), follow=True
        )
        response = self.client.post(
            reverse('posts:post_publish', args=[post.pk])
        )
        # Check that the response is 403 Forbiddden
        self.assertEqual(response.status_code, 403)


class TestPostSearch(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='jesus', email='jesus@nazareth', password='secret'
        )

    def test_post_search(self):
        create_post('hello world', self.admin, is_draft=False)
        response = self.client.get(reverse('posts:post_search') + '?q=hello')
        self.assertQuerysetEqual(
            response.context['posts'], ['<Post: hello world>']
        )


class TestTagView(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='jesus', email='jesus@nazareth', password='secret'
        )

    def test_shows_posts_with_matching_tags(self):

        tag = Tag.objects.create(name='programming')

        post = create_post('Test', self.admin, is_draft=False)
        post.save()
        post.tags.add(tag)

        draft = create_post('Draft', self.admin, is_draft=True)
        draft.save()
        draft.tags.add(tag)

        response = self.client.get(tag.get_absolute_url())

        self.assertQuerysetEqual(response.context['posts'], ['<Post: Test>'])
