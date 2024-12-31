#!/usr/bin/env python3
# entrypoint.py

import os
import sys
import datetime
from linode_api4 import LinodeClient

# _id = str(uuid.uuid4()).split('-')[0]
date = datetime.datetime.now().replace(microsecond=0).isoformat()

# params = {
#     'token': os.environ.get('TOKEN'),
#     'ltype': os.environ.get('TYPE'),
#     'region': os.environ.get('REGION'),
#     'image': os.environ.get('IMAGE'),
#     'authorized_keys': os.environ.get('SSH_KEY'),
#     'label': os.environ.get('LABEL'),
#     'private_ip': os.environ.get('PRIVATE_IP'),
#     'firewall_id': os.environ.get('FIREWALL_ID'),
#     'tag': [os.environ.get('TAG')], # update
#     'user_data': os.environ.get('USER_DATA')
# }

def _var(env: str) -> str:
    _input = {env}
    is_set = _input.intersection(os.environ)

    if is_set:
        return os.environ.get(env)


def _params():
    # args = [_var('TYPE'), _var('REGION')]
    params = {
        'ltype': _var('TYPE'),
        'region': _var('REGION'),
        'image': _var('IMAGE'),
        'authorized_keys': _var('SSH_KEY'),
        'label': _var('LABEL'),
        'booted': True,
        'tags': [_var('TAG')],
        'private_ip': bool(_var('PRIVATE_IP'))
    }

    if _var('USER_DATA'):
        metadata = {
            'user_data': _var('USER_DATA'),
            'encode_user_data': False
        }
        params['metadata'] = metadata

    if _var('FIREWALL_ID'):
        params['firewall'] = int(_var('FIREWALL_ID'))

    return params
   

def create_linode():
    '''Deploy a Linode instance'''
    token = _var('TOKEN')
    client = LinodeClient(token)
    instance, _ = client.linode.instance_create(**_params())
    # metadata = {
    #     'user_data': params['user_data'],
    #     'encode_user_data': False
    # }
    # if params['firewall_id']:
    #     firewall = params['firewall_id']
    # else:
    #     firewall = None

    # instance, _ = instance_create(**_params())
    # instance, _ = instance_create(
    #                             ltype=params['type'],
    #                             region=params['region'],
    #                             image=params['image'],
    #                             authorized_keys=params['ssh_key'],
    #                             label=params['label'],
    #                             booted=True,
    #                             tags=[params['tag']],
    #                             private_ip=bool(params['private_ip']),
    #                             metadata=metadata,
    #                             firewall=(params['firewall_id'])
    # )

    if instance.status == 'provisioning':
        return instance


def main():
    try:
        linode = create_linode()
        with open(os.environ['GITHUB_OUTPUT'], 'a+') as f:
            print(f'linode-id={linode.id}', file=f)
            f.seek(0)
            last_line = f.readlines()[-1]
            print(last_line)
    except Exception as err:
        print(err)
        sys.exit(1)


# main
if __name__ == '__main__':
    main()
