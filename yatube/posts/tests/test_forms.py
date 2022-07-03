
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.forms import PostForm


User = get_user_model()


class FormPostTests(TestCase):
    '''Класс для тестирования форм'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.form = PostForm
        cls.group = Group.objects.create(
            title='ТЕстовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_post = {
            'text': 'Текст создаваемого поста',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_post, follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                ('posts:profile'),
                kwargs={'username': f'{self.user.username}'}
            )
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Тестовый пост').exists())

    def test_post_edit(self):
        posts_count = Post.objects.count()
        form_post = {
            'text': 'Текст изменённого поста',
        }
        response = self.authorized_client.post(
            reverse(('posts:edit'), kwargs={'post_id': f'{self.post.id}'}),
            data=form_post,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                ('posts:post_detail'),
                kwargs={'post_id': f'{self.post.id}'}
            )
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(text='Текст изменённого поста').exists()
        )
