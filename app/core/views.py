from django.shortcuts import render


def main_page_view(request):
    """Display the main page."""
    return render(request, 'main_page.html')


def error_handler(request, exception=None, code=None, message=None):
    """Generic error handler view."""

    return render(request, 'error.html', {
        'code': code,
        'message': message
    }, status=code)


def handler400(request, exception=None):
    return error_handler(request, exception, 400, 'Bad Request')


def handler403(request, exception=None):
    return error_handler(request, exception, 403, 'Access Denied')


def handler404(request, exception=None):
    return error_handler(request, exception, 404, 'Page Not Found')


def handler500(request, exception=None):
    return error_handler(request, exception, 500, 'Server Error')
