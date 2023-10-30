from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, redirect

from .models import Device


@login_required
def index(request):
    devices = Device.objects.all()
    paginator = Paginator(devices, int(request.GET.get("per_page", "20")))
    page = int(request.GET.get("page", "1"))
    try:
        devices = paginator.page(page)
    except (EmptyPage, InvalidPage):
        devices = paginator.page(paginator.num_pages)
    context = {
        "devices": devices,
    }
    return render(request, "remote/index.html", context)
