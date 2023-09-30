from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, redirect

from .api import wg_overwrite, wg_get
from .models import Server, Client


@login_required
def index(request):
    context = {
        "servers": Server.objects.all(),
        "clients": Client.objects.filter(user_id=request.user.id),
        "wireguard": {
            "allowed_ips": settings.WIREGUARD_ALLOWED_IPS
        }
    }
    return render(request, "wireguard/index.html", context)


@login_required
@staff_member_required
def server(request):
    wireguard_server_objects = Server.objects.all()
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        server = Server.objects.get(id=int(id))
        if "inactive" in request.POST:
            server.is_active = False
            server.save()
        elif "active" in request.POST:
            server.is_active = True
            server.save()
        elif "register" in request.POST:
            wg_overwrite(server)
        elif "list" in request.POST:
            res = wg_get(server)
            return render(request, "wireguard/server.html", {'res': res})
        return redirect('/wireguard/server')

    paginator = Paginator(wireguard_server_objects, int(request.GET.get("per_page", "5")))
    page = int(request.GET.get("page", "1"))
    try:
        servers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        servers = paginator.page(paginator.num_pages)
    context = {
        "servers": servers,
    }
    return render(request, "wireguard/server.html", context)