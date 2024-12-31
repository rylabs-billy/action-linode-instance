[![GitHub License](https://img.shields.io/github/license/rylabs-billy/action-linode-instance?style=plastic)](https://github.com/rylabs-billy/action-linode-instance/blob/main/LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/rylabs-billy/action-linode-instance/test.yml?branch=main&style=plastic&logo=github&link=https%3A%2F%2Fgithub.com%2Frylabs-billy%2Faction-linode-instance%2Factions%2Fworkflows%2Ftest.yml)](https://github.com/rylabs-billy/action-linode-instance/actions/workflows/test.yml)
[![GitHub Marketplace](https://img.shields.io/badge/marketplace-action--linode--instance-blue?style=plastic&logo=github)](https://github.com/marketplace/actions/linode-github-actions-runner)

# Linode Instance GitHub Action

Provisions a Linode VM on Akamai Cloud. Can be used with [action-runner-userdata](https://github.com/rylabs-billy/action-runner-userdata) for a self-hosted runner, or for any other reason you'd need to spin up a quick VM for testing.

____
* [Usage](#usage)
* [Inputs](#inputs)
  * [token](token)
  * [label](#label)
  * [ssh-key](#ssh-key)
  * [image](#image)
  * [user-data](#user-data)
  * [private-ip](#private-ip)
  * [region](#region)
  * [type](#type)
  * [firewall-id](#firewall-id)
  * [tag](#tag)
* [Outputs](#outputs)
* [Contributing](#contributing)

## Usage
At minimum you need to supply a [Linode API
token](https://techdocs.akamai.com/cloud-computing/docs/manage-personal-access-tokens)
with `write` permission for `Linodes`. Your Linode token should be stored as an
encrypted GitHub secret to ensure it's secured and sanitized from workflow
outputs. Default values will be used for the other required inputs.

```yaml
- name: Linode instance
  uses: rylabs-billy/action-linode-instance@v1
  with:
    token: ${{ secrets.LINODE_TOKEN }}
```

Optional inputs include `firewall-id`, `ssh-key`, `user-data` (cloud-init), and
a `tag` for your instance. Cloud-init user-data must be a
[cloud-config](https://www.linode.com/docs/guides/configure-and-secure-servers-with-cloud-init/#create-a-cloud-config-file)
file as a [base64 encoded](https://www.linode.com/docs/guides/configure-and-secure-servers-with-cloud-init/#deploy-an-instance-with-user-data)
string. The value for `firewall-id` must be the ID of an existing [Cloud Firewall.](https://techdocs.akamai.com/cloud-computing/docs/getting-started-with-cloud-firewalls)

```yaml
- name: Linode instance
  uses: rylabs-billy/action-linode-instance@v1
  with:
    token: ${{ secrets.LINODE_TOKEN }}
    ssh-key: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5A bthompson@linode.com
    user-data: aG9vcmF5IGZvciBsaW5vZGUgYW5kIGhvb3JheSBmb3IgZ2l0aHViIGFj
    firewall-id: 12345
    tag: test
```

Advanced example of customizing all possible inputs (overriding all defaults) and passing the `linode-id` output to the next step.

```yaml
name: Linode test

on:
  push:
    branches:
      - main

jobs:
  linode-instance:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Deploy Linode
        id: linode
        uses: rylabs-billy/action-linode-instance@v1
        with:
          token: ${{ secrets.LINODE_TOKEN }}
          label: testing_linode
          ssh-key: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5A bthompson@linode.com
          image: linode/debian12
          user-data: aG9vcmF5IGZvciBsaW5vZGUgYW5kIGhvb3JheSBmb3IgZ2l0aHViIGFj
          private-ip: false
          region: ap-south
          type: g6-standard-8
          firewall-id: 12345
          tag: test

      - name: Print Linode ID
        shell: bash
        run: |-
          echo "The Linode ID is: $LINODE_ID"
        env:
          LINODE_ID: ${{ fromJson(steps.linode.outputs.linode-id) }}
```

## Inputs
This GitHub Action takes the following inputs:

### `token`
The Linode API Personal Access Token to authenticate with.

### `label`
Human readable label for the Linode instance. \
Default: **linode-action**

### `ssh-key`
Public SSH key to access the Linode (optional).

### `image`
Linux image to provision Linode with. \
Default: **linode/ubuntu22.04**

### `user-data`
Cloud-init base64 encoded user-data (optional).

### `private-ip`
Add a private IP to the Linode instance. \
Default: **true**

### `region`
Region where the Linode will be deployed. \
Default: **us-ord**

### `type`
Type of Linode instance to be created. \
Default: **g6-standard-4**

### `firewall-id`
Cloud Firewall to attach the Linode instance (optional).

### `tag`
Tag for your Linode Instance (optional).

## Outputs
### `linode-id`
Linode instance ID

## Contributing
You want to improve **action-linode-instance**! 😍 

Please open a [GitHub issue](../../issues/new/choose) to report bugs or suggest features, or follow the [fork and pull model](https://opensource.guide/how-to-contribute/#opening-a-pull-request) for open source contributions.
