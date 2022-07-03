from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    '''Тестируем модели Post и Group
    на корректную работу __str__'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='БАГульники',
            slug='Тестовый слаг',
            description='Кто ищёт - тот найдёт!',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        model_post = PostModelTest.post
        model_group = PostModelTest.group
        models_dict = {
            model_post: model_post.text[:15],
            model_group: model_group.title
        }
        for model, expected_value in models_dict.items():
            with self.subTest(model=model):
                self.assertEqual(
                    model.__str__(), expected_value,
                    'метод __str__ работает не верно'
                )
