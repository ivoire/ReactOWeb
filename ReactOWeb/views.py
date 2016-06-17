import datetime
import dateutil.parser
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.http import urlencode

from ReactOWeb.models import Message


def home(request):
    return render(request, 'ReactOWeb/home.html', {})


def charts(request):
    topics = Message.objects.values('topic').annotate(count=Count('topic'))
    return render(request, "ReactOWeb/charts.html",
                  {"topics": topics})


def messages(request):
    # Filter if requested
    field = request.GET.get("field", None)
    value = request.GET.get("value", None)
    query = Message.objects.order_by('-datetime')
    get_string = ""

    if field is not None and value is not None:
        if field == 'topic':
            query = query.filter(topic=value)
        elif field == 'username':
            query = query.filter(username=value)
        else:
            return HttpResponseBadRequest()

        get_string = urlencode({"field": field, "value": value})

    # Show the right page
    paginator = Paginator(query, 25)
    try:
        page = paginator.page(request.GET.get('page', 1))
    except (PageNotAnInteger, EmptyPage):
        return HttpResponseBadRequest()

    return render(request, 'ReactOWeb/messages.html',
                  {'messages': page,
                   'get_string': get_string})


def messages_details(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'ReactOWeb/message.html',
                  {'message': message})


def api_messages(request):
    # Apply datetime>= and dateimt<=
    datetime_gt = request.GET.get('datetime>', None)
    datetime_lt = request.GET.get('datetime<', None)

    query = Message.objects.all()
    if datetime_gt is not None:
        # TODO: handle crashes
        dt_gt = dateutil.parser.parse(datetime_gt)
        query = query.filter(datetime__gt=dt_gt)
    if datetime_lt is not None:
        # TODO: handle crashes
        dt_lt = dateutil.parser.parse(datetime_lt)
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
