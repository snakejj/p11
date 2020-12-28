from django.http import JsonResponse, HttpResponseNotFound

from .helpers import get_completions


def complete(request):
    """Returns a list of terms in a json format for jquery-ui autocomplete."""
    term = request.GET.get("term")

    terms = get_completions(term)
    return JsonResponse(terms, safe=False)
