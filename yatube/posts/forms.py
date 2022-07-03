from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    '''Класс для формы создания поста'''

    class Meta:

        model = Post
        fields = ('text', 'group')
        labels = {'text': 'Текст поста', 'group': 'Группа поста'}
        help_texts = {
            'text': 'Текст создаваемого поста',
            'group': 'Выбор группы для поста',
        }
