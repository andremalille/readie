from django.shortcuts import render


def main_page_view(request):
    """Display the main page."""
    return render(request, 'main_page.html')
