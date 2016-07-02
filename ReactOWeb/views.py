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
    # Filter the topic if requested
    topic_prefix = request.GET.get("topic", None)
    base_query = Message.objects.all()
    if topic_prefix is not None:
        base_query = Message.objects.filter(topic__startswith=topic_prefix)

    # Messages for the last day, hour-by-hour
    now = datetime.utcnow().replace(tzinfo=utc)
    messages_by_hours = []
    now_hours = datetime(now.year, now.month, now.day, now.hour, tzinfo=utc)
    for hour in range(23, 0, -1):
        dt_begin = now_hours - timedelta(hours=hour)
        dt_end = now_hours - timedelta(hours=(hour - 1))
        count = base_query.filter(datetime__range=(dt_begin, dt_end)).count()
        messages_by_hours.append(("%dh" % dt_begin.hour, count))
    # Get the last interval (now_hours to now)
    count = base_query.filter(datetime__range=(now_hours, now)).count()
    messages_by_hours.append(('now', count))

    # Messages for the last month, day-by-day
    now = datetime.utcnow().replace(tzinfo=utc)
    messages_by_days = []
    now_days = datetime(now.year, now.month, now.day, tzinfo=utc)
    for day in range(30, 0, -1):
        dt_begin = now_days - timedelta(days=day)
        dt_end = now_days - timedelta(days=(day - 1))
        count = base_query.filter(datetime__range=(dt_begin, dt_end)).count()
        messages_by_days.append((dt_begin.strftime('%b %d'), count))
    count = base_query.filter(datetime__range=(now_days, now)).count()
    messages_by_days.append(('today', count))

    # List of topics
    topics = base_query.filter(datetime__gt=(now - timedelta(days=30)))
    topics = topics.values('topic').annotate(count=Count('topic'))
    topics = topics.order_by('topic')

    return render(request, "ReactOWeb/charts.html",
                  {"messages_by_hours": messages_by_hours,
                   "messages_by_days": messages_by_days,
                   "topics": topics})


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
