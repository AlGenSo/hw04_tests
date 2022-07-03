from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    '''Класс для тестирования URL'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='ТЕстовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
            group=cls.group,
            id='7',
        )

    def setUp(self):
        self.guest_client = Client()
        self.guest = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.guest)
        self.user = User.objects.get(username='auth')
        self.author_client = Client()
        self.author_client.force_login(self.user)

    def the_test_page_is_available_only_to_the_author(self):
        response = self.author_client.get('/posts/7/edit')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test-slug/',
            'posts/profile.html': '/profile/auth/',
            'posts/post_detail.html': '/posts/7/',
            'posts/post_create.html': '/create/'
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                if self.authorized_client:
                    response = self.authorized_client.get(adress)
                    self.assertTemplateUsed(response, template)
                else:
                    response = self.guest_client.get(adress)
                    self.assertTemplateUsed(response, template)

    def test_request_to_a_non_existent_page(self):
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
