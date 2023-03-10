from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import Post, Author
from datetime import date

class PostFilter(FilterSet):

    title = CharFilter(
        field_name='title',
        label='Название',
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        lookup_expr='pk',
        label='Автор',
        empty_label='Все авторы',
    )

    class Meta:
        model = Post
        fields = []

    @property
    def qs(self):
        parent = super().qs

        if 'datetime_in' in self.data:
            try:
                date_iso = date.fromisoformat(f"{self.data['datetime_in']}")
                return parent.filter(datetime_in__gt=date_iso)
            except ValueError:
                return parent.all()
        else:
            return parent.all()



