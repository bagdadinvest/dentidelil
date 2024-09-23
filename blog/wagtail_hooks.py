from wagtail.core import hooks
from django.urls import path
from django.http import JsonResponse
from .models import AIContentTemplate

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('get-snippet-content/<int:snippet_id>/', get_snippet_content, name='get_snippet_content'),
    ]

def get_snippet_content(request, snippet_id):
    try:
        snippet = AIContentTemplate.objects.get(id=snippet_id)
        content = {
            'title': snippet.name,  # You can customize this mapping
            'body': snippet.prompt_template,  # For example, using the prompt_template as body content
        }
        return JsonResponse({'content': content})
    except AIContentTemplate.DoesNotExist:
        return JsonResponse({'error': 'Snippet not found'}, status=404)
