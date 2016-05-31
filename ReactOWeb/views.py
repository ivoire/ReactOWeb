import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from ReactOWeb.models import Message


def api_messages(request):
    # Get the limits and bounds
    page = request.GET.get('page', 0)
    limit = request.GET.get('limit', None)

    if limit is not None:
        try:
            page = int(page)
            limit = int(limit)
        except ValueError:
            return HttpResponseBadRequest()
        if page < 0 or limit < 0:
            return HttpResponseBadRequest()
        query = Message.objects.all()[page*limit:(page+1)*limit]
    else:
        query = Message.objects.all()

    messages = [m.as_dict() for m in query]
    return HttpResponse(json.dumps(messages), content_type="application/json")


def api_messages_details(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return HttpResponse(json.dumps(message.as_dict()), content_type="application/json")
