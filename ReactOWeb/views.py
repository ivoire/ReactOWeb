from datetime import timedelta
import dateutil.parser
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.http import urlencode
from django.utils.timezone import datetime, utc

from ReactOWeb.models import Message


def home(request):
    return render(request, 'ReactOWeb/home.html', {})


def charts(request):
    # List of topics
    topics = Message.objects.values('topic').annotate(count=Count('topic'))

    # Messages for the last day, hour-by-hour
    now = datetime.utcnow().replace(tzinfo=utc)
    messages_by_hours = []
    for hour in range(24, 0, -1):
        count = Message.objects.filter(datetime__range=(now-timedelta(0, hour * 3600), now-timedelta(0, (hour - 1) * 3600))).count()
        messages_by_hours.append((hour, count))

    # Messages for the last month, day-by-day
    now = datetime.utcnow().replace(tzinfo=utc)
    messages_by_days = []
    for day in range(30, 0, -1):
        count = Message.objects.filter(datetime__range=(now-timedelta(day), now-timedelta(day - 1))).count()
        messages_by_days.append(((now-timedelta(day)).strftime('%b %d'), count))

    return render(request, "ReactOWeb/charts.html",
                  {"topics": topics,
                   "messages_by_hours": messages_by_hours,
                   "messages_by_days": messages_by_days})


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


def messages_live(request):
    return render(request, 'ReactOWeb/messages_live.html',
                  {'messages': Message.objects.order_by('-datetime')[0:30]})


def api_messages(request):
    # Apply datetime>= and dateimt<=
    datetime_gt = request.GET.get('datetime>', None)
    datetime_lt = request.GET.get('datetime<', None)

    query = Message.objects.order_by('-datetime')
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
