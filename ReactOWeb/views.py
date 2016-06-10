import datetime
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from ReactOWeb.models import Message


def home(request):
    return render(request, 'ReactOWeb/home.html', {})


def api_messages(request):
    # Apply datetime>= and dateimt<=
    datetime_gt = request.GET.get('datetime>', None)
    datetime_lt = request.GET.get('datetime<', None)

    query = Message.objects.all()
    if datetime_gt is not None:
        # TODO: handle crashes
        dt_gt = datetime.datetime.strptime(datetime_gt, '%Y-%m-%dT%H:%M:%S.%f')
        query = query.filter(datetime__gt=dt_gt)
    if datetime_lt is not None:
        # TODO: handle crashes
        dt_lt = datetime.datetime.strptime(datetime_lt, '%Y-%m-%dT%H:%M:%S.%f')
        query = query.filter(datetime__lt=dt_lt)

    # Apply limit= and page=
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
        query = query[page*limit:(page+1)*limit]

    messages = [m.as_dict() for m in query]
    return HttpResponse(json.dumps(messages), content_type="application/json")


def api_messages_details(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return HttpResponse(json.dumps(message.as_dict()),
                        content_type="application/json")
