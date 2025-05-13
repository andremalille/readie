from django import forms
from core.models import BookList


class BookForm(forms.ModelForm):
    """Form for creating and updating book lists"""
    class Meta:
        model = BookList
        fields = ('status', 'favourites', 'pages_read')

    def __init__(self, *args, **kwargs):
        book_instance = kwargs.pop('book_instance', None)
        super().__init__(*args, **kwargs)
        if book_instance:
            self.instance.book = book_instance

    def clean_pages_read(self):
        pages_read = self.cleaned_data.get('pages_read')
        num_pages = self.instance.book.num_pages
        if pages_read is not None and num_pages is not None:
            if pages_read > num_pages:
                raise forms.ValidationError(
                    f"You cannot read more pages "
                    f"({pages_read}) than the book has ({num_pages})."
                )
            if pages_read < 0:
                raise forms.ValidationError(
                    "You entered an invalid pages read value."
                )

        return pages_read


class BookSearchForm(forms.Form):
    """Form for searching and filtering books"""
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
