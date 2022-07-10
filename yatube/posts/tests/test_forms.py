from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.forms import PostForm


class FormPostTests(TestCase):
    '''Класс для тестирования форм'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.form = PostForm
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_an_authorized_user_can_create_a_post(self):
        '''Валидная форма создает запись в Post
        авторизованным пользователем'''
        posts_count = Post.objects.count()
        form_post = {
            'text': 'Текст создаваемого поста',
            'group': self.group.id,
        }
        post = Post.objects.first()
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_post, follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                ('posts:profile'),
                kwargs={'username': self.user.username}
            )
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.group.id, self.group.id)
        self.assertEqual(post.author, self.user)

    def test_an_authorized_user_can_edit_the_post(self):
        '''При отправке валидной формы авторизованным пользователем
        со страницы редактирования поста происходит изменение поста'''
        posts_count = Post.objects.count()
        form_post = {
            'text': 'Текст изменённого поста',
            'group': self.group.id,
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
            Post.objects.filter(
                id=self.post.id,
                text='Текст изменённого поста',
                group=self.group.id,
            ).exists()
        )
