import ipaddress

from django import template
from django.conf import settings
from pytz import timezone
import markdown as md

register = template.Library()


@register.simple_tag
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.simple_tag
def wg_v4(v4, count):
    return ipaddress.ip_address(v4) + count - 1


@register.simple_tag
def url_replace(request, **kwargs):
    params = request.GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    return params.urlencode()


@register.simple_tag
def time_to_str(time):
    if time is None:
        return "無期限"
    time_format = "%Y/%m/%d %H:%M:%S"
    return time.astimezone(timezone(settings.TIME_ZONE)).strftime(time_format)


@register.simple_tag
def to_int(value):
    if not value:
        return None
    return int(value)


@register.simple_tag
def beta():
    return settings.BETA


@register.simple_tag
def debug():
    return settings.DEBUG


@register.simple_tag
def array_to_str(data):
    return ', '.join(data)
