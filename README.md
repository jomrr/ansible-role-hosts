# Ansible Role: hosts

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-hosts)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-hosts)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-hosts)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-hosts/dev.yml?branch=dev&event=push&label=dev)](https://github.com/jomrr/ansible-role-hosts/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-hosts/main.yml?branch=main&event=push&label=main)](https://github.com/jomrr/ansible-role-hosts/actions/workflows/main.yml?query=branch%3Amain)

Ansible role for managing local host name resolution in /etc/hosts.

## Purpose

Manage /etc/hosts for local name resolution. The role replaces the complete
file with stable loopback records, local host records, and hosts_entries.
Repeated runs with unchanged inputs and address facts are idempotent.

## Scope

### Managed

- IPv4 and IPv6 loopback records and local hostname mappings.
- Additional canonical hostnames and aliases from hosts_entries.
- File ownership, permissions, and module-provided backups.

### Not Managed

- Routing, network connectivity, DHCP clients, DNS servers, or the system
  hostname.
- Preservation of entries not described by the role inputs.

## Requirements

- Gather Ansible facts before applying the role.
- The role must be the sole writer of /etc/hosts; disable runtime management of
  that file in containers.

## Dependencies

```yaml
collections:
  - name: community.general
    version: '>=12.0.0'
```

## Role Variables

### `hosts_backup`

Type: `bool`. Required: `false`.

Back up /etc/hosts when its contents change.

Default:

```yaml
hosts_backup: true
```

### `hosts_domain`

Type: `str`. Required: `false`.

Domain appended to the short hostname; an empty string omits the FQDN.

Default:

```yaml
hosts_domain: '{{ ansible_facts.domain }}'
```

### `hosts_ip_all`

Type: `bool`. Required: `false`.

Add all gathered non-loopback IPv4 and IPv6 addresses; overrides the
single-address options.

Default:

```yaml
hosts_ip_all: false
```

### `hosts_ip_static`

Type: `bool`. Required: `false`.

Use hosts_ip_address directly instead of selecting 127.0.1.1 for a DHCP default
route.

Default:

```yaml
hosts_ip_static: false
```

### `hosts_ip_address`

Type: `str`. Required: `false`.

Single host address; defaults to the gathered IPv4 address, or 127.0.1.1 when
unavailable.

Default:

```yaml
hosts_ip_address: '{{ ansible_facts.default_ipv4.address | default(''127.0.1.1'')
  }}'
```

### `hosts_entries`

Type: `list`. Required: `false`.

Additional IPv4 or IPv6 records in the supplied order.

Default:

```yaml
hosts_entries: []
```

## Managed Files

- `/etc/hosts`

## Check Mode

Supports check mode with the same address selection as a normal run.

- Automatic address selection requires iproute to be installed before a first
  check-mode run.
- Explicit hosts_ip_static and hosts_ip_address inputs need no route information
  or iproute installation.

## Service Behavior

No service is managed or restarted. Changed hosts records refresh Ansible facts
through a handler.

### Handlers

- Refresh Ansible facts after /etc/hosts changes.

## Security Notes

- The hosts file is owned by root with mode 0644; backups are enabled by
  default.

## Operational Notes

- hosts_ip_all takes precedence and adds all gathered non-loopback IPv4 and IPv6
  addresses.
- Automatic single-address selection uses 127.0.1.1 for a DHCP default route and
  hosts_ip_address otherwise.
- Without a gathered default IPv4 address, hosts_ip_address defaults to
  127.0.1.1.
- Route information is read only to choose a hosts record; the role does not
  test or modify routing.
- No portable native validator for a candidate hosts file is used; the argument
  schema validates input structure.
- Physical machines and virtual machines are managed without
  virtualization-based exclusions.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
| --------- | ------------ | ------- | --------------- |
| RedHat | AlmaLinux | latest | [jomrr/molecule-almalinux:latest](https://hub.docker.com/r/jomrr/molecule-almalinux) |
| Debian | Debian | latest | [jomrr/molecule-debian:latest](https://hub.docker.com/r/jomrr/molecule-debian) |
| RedHat | Fedora | latest | [jomrr/molecule-fedora:latest](https://hub.docker.com/r/jomrr/molecule-fedora) |
| Suse | OpenSuse Leap | latest | [jomrr/molecule-opensuse-leap:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-leap) |
| Suse | OpenSuse Tumbleweed | latest | [jomrr/molecule-opensuse-tumbleweed:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-tumbleweed) |
| Debian | Ubuntu | latest | [jomrr/molecule-ubuntu:latest](https://hub.docker.com/r/jomrr/molecule-ubuntu) |

## Example Playbook

### Automatic local host records

Use gathered address facts and add a record with an alias.

```yaml
- name: Configure local name resolution
  hosts: all
  gather_facts: true
  roles:
    - role: jomrr.hosts
      hosts_entries:
        - ip: 192.0.2.15
          name: application.example.org
          aliases: [application]
```

### Explicit local address

Write a chosen host address independently of the routing configuration.

```yaml
- name: Configure an explicit local host record
  hosts: all
  gather_facts: true
  roles:
    - role: jomrr.hosts
      hosts_ip_static: true
      hosts_ip_address: 192.0.2.20
      hosts_domain: example.org
```

### All local addresses

Map the short hostname and FQDN to every gathered IPv4 and IPv6 address.

```yaml
- name: Configure all local host addresses
  hosts: all
  gather_facts: true
  roles:
    - role: jomrr.hosts
      hosts_ip_all: true
```

## Author

[Jonas Mauer](https://github.com/jomrr)

## License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for the full license text.

Copyright (c) 2020 Jonas Mauer.
