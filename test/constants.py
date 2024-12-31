# test/constants.py

from entrypoint import (
    _var,
    date
)

TOKEN = _var('TOKEN')


# custom metaclass to make class attributes immutable
class Meta(type):
    def __setattr__(cls, name, value):
        for v in vars(cls):
            if name == v:
                raise AttributeError(f'Cannot modify attribute {v}')
            super().__setattr__(name, value)


class MockHTTP(metaclass=Meta):
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "test-client",
    }
    RESP = {
        "alerts": {
            "cpu": 180,
            "io": 10000,
            "network_in": 10,
            "network_out": 10,
            "transfer_quota": 80
        },
        "backups": {
            "available": "true",
            "enabled": "true",
            "last_successful": date,
            "schedule": {
                "day": "Saturday",
                "window": "W22"
            }
        },
        "created": date,
        "has_user_data": "true",
        "host_uuid": "3a3ddd59d9a78bb8de041391075df44de62bfec8",
        "hypervisor": "kvm",
        "id": 12345,
        "image": _var('IMAGE'),
        "ipv4": [
            "203.0.113.1",
            "192.0.2.1"
        ],
        "ipv6": "c001:d00d::1337/128",
        "label": _var('LABEL'),
        "placement_group": {
            "id": 528,
            "label": "PG_Miami_failover",
            "placement_group_policy": "strict",
            "placement_group_type": "anti-affinity:local"
        },
        "region": _var('REGION'),
        "specs": {
            "disk": 81920,
            "gpus": 0,
            "memory": 4096,
            "transfer": 4000,
            "vcpus": 2
        },
        "status": "provisioning",
        "tags": _var('TAG'),
        "type": _var('TYPE'),
        "updated": date,
        "watchdog_enabled": "true"
    }
    ERR_RESP = {"errors": [{"reason": "Invalid Token"}]}


class Path(metaclass=Meta):
    CA_PATH = "/mock/ca"
    ENDPOINT = "https://api.linode.com/v4/linode/instances"
