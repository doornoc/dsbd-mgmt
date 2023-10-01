import ipaddress

import requests
import json

from django.core.serializers.json import DjangoJSONEncoder

from mgmt.wireguard.models import Client, Server


def wg_create(client):
    servers = Server.objects.filter(is_active=True)
    for server in servers:
        url = 'http://%s:%d/api/v1/peer' % (server.mgmt_ip, server.mgmt_port)
        requests.post(url, data=json.dumps({
            "public_key": client.public_key,
            "allowed_ips": [str(ipaddress.ip_address(server.start_ip) + client.count - 1) + "/32"]
        }), headers={'Content-Type': 'application/json'})


def wg_update(old_public_key, client):
    servers = Server.objects.filter(is_active=True)
    for server in servers:
        url = 'http://%s:%d/api/v1/peer' % (server.mgmt_ip, server.mgmt_port)
        requests.put(url, data=json.dumps({
            "old_public_key": old_public_key,
            "client": {
                "public_key": client.public_key,
                "allowed_ips": [str(ipaddress.ip_address(server.start_ip) + client.count - 1) + "/32"]
            },
        }), headers={'Content-Type': 'application/json'})


def wg_delete(public_key):
    servers = Server.objects.all()
    for server in servers:
        url = 'http://%s:%d/api/v1/peer' % (server.mgmt_ip, server.mgmt_port)
        requests.delete(url, data=json.dumps({"public_key": public_key}), headers={'Content-Type': 'application/json'})


def wg_delete_all(server):
    url = 'http://%s:%d/api/v1/peer/all' % (server.mgmt_ip, server.mgmt_port)
    requests.delete(url)


def wg_overwrite(server):
    clients = Client.objects.all()
    url = 'http://%s:%d/api/v1/peer/all' % (server.mgmt_ip, server.mgmt_port)
    tmp_clients = []
    for client in clients:
        tmp_clients.append({
            "public_key": client.public_key,
            "allowed_ips": [str(ipaddress.ip_address(server.start_ip) + client.count - 1) + "/32"]
        })
    requests.put(url, data=json.dumps({"clients": tmp_clients}), headers={'Content-Type': 'application/json'})


def wg_overwrite_all():
    servers = Server.objects.filter(is_active=True)
    clients = Client.objects.all()
    for server in servers:
        url = 'http://%s:%d/api/v1/peer/all' % (server.mgmt_ip, server.mgmt_port)
        tmp_clients = []
        for client in clients:
            tmp_clients.append({
                "public_key": client.public_key,
                "allowed_ips": [str(ipaddress.ip_address(server.start_ip) + client.count - 1) + "/32"]
            })
        print(json.dumps({"clients": tmp_clients}))
        requests.put(url, data=json.dumps({"clients": tmp_clients}), headers={'Content-Type': 'application/json'})


def wg_get(server):
    url = 'http://%s:%d/api/v1/peer' % (server.mgmt_ip, server.mgmt_port)
    res = requests.get(url, headers={'Content-Type': 'application/json'})
    return res.text
