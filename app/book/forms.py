from django import forms
from core.models import BookList


class BookForm(forms.ModelForm):
    class Meta:
        model = BookList
        fields = ('category',)

    def __init__(self, *args, **kwargs):
        book_instance = kwargs.pop('book_instance', None)
        super().__init__(*args, **kwargs)
        if book_instance:
            self.instance.book = book_instance


class BookSearchForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
