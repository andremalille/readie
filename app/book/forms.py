from django import forms
from core.models import BookList


class BookForm(forms.ModelForm):
    class Meta:
        model = BookList
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        book_instance = kwargs.pop('book_instance', None)
        super().__init__(*args, **kwargs)
        if book_instance:
            self.instance.book = book_instance


class BookSearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        required=False,
        help_text="Search by book title, author or ISBN10 and ISBN13",
    )

    categories = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )
    statuses = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=BookList.STATUS_CHOICES,
    )
    pages_min = forms.IntegerField(label='Min pages', required=False)
    pages_max = forms.IntegerField(label='Max pages', required=False)
    rating_min = forms.DecimalField(
        label='Min rating', required=False,
        max_digits=3, decimal_places=2
    )
    rating_max = forms.DecimalField(
        label='Max rating', required=False,
        max_digits=3, decimal_places=2
    )
    year_min = forms.IntegerField(label='Min year', required=False)
    year_max = forms.IntegerField(label='Max year', required=False)
