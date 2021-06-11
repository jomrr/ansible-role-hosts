# ansible-role-hosts

![GitHub](https://img.shields.io/github/license/jam82/ansible-role-hosts) ![GitHub last commit](https://img.shields.io/github/last-commit/jam82/ansible-role-hosts) ![GitHub issues](https://img.shields.io/github/issues-raw/jam82/ansible-role-hosts) ![Travis (.com) branch](https://img.shields.io/travis/com/jam82/ansible-role-hosts/main?label=ansible-lint%20latest)

**Ansible role for configuring the `/etc/hosts` file.**

## Supported Platforms

- Alpine
- Amazon
- Archlinux
- CentOS
- Debian
- Fedora
- Manjaro
- OracleLinux
- OpenSuse Leap, Tumbleweed
- Raspbian
- Ubuntu

## Requirements

Ansible 2.9 or higher.

## Variables

Variables and defaults for this role.

### defaults/main.yml

```yaml
# The role is disabled by default, so you do not get in trouble.
# Checked in tasks/main.yml which includes tasks.yml if enabled.
hosts_role_enabled: false

# Backup the hosts file when applying template
hosts_backup: true

# Set domain for FQDN in hosts file.
# Only overwrite this if you want to force the domain manually.
# Normally ansible_domain should be set if you have a sane network configuration.
hosts_domain: "{{ (ansible_domain | length > 0) | ternary(ansible_domain, '') }}"

# Determine how the targeted host(s) is added to /etc/hosts
# hosts_ip_all:
#   true  = generates entries for all IPs in ansible_all_ipvX_addresses
#           with ansible_fqdn and ansible_hostname
#   false = generates single entry for value of key "address"
#           with ansible_fqdn and ansible_hostname dependant on static setting
hosts_ip_all: false
# hosts_ip_static:
#   true  = use address defined in key "address"
#   false = use 127.0.1.1 if IP obtained via dhcp.
#           If IP is not obtained by dhcp the value of key "address" is used.
hosts_ip_static: false
# hosts_ip_static:
#   IP address to use, when "hosts_ip_all: false", and
#   "hosts_ip_static: true" or "static: false" and IP not obtained via dhcp
#   If "static: false" and IP was obtained via dhcp then 127.0.1.1 is used
hosts_ip_address: "{{ ansible_default_ipv4.address }}"

# Additional entries in the hosts file
# hosts_entries:
#   - name: test.blabla.tld
#     aliases:
#       - test
#       - sys01.blabla.tld
#     ip: 192.168.08.15
#   - name: test6.blabla.tld
#     aliases:
#       - test6
#     ip: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
hosts_entries: []
```

## Dependencies

None.

## Example Playbooks

Here are some example configurations.

### Systems with one interface and single IP address

```yaml
---
# role: ansible-role-hosts
# file: site.yml

- hosts: all
  become: true
  gather_facts: true
  vars:
    hosts_role_enabled: true
  roles:
    - role: ansible-role-hosts
```

### Force static IP in /etc/hosts even if obtained by dhcp

```yaml
---
# role: ansible-role-hosts
# file: site.yml

- hosts: all
  become: true
  gather_facts: true
  vars:
    hosts_role_enabled: true
    hosts_ip_static: true
  roles:
    - role: ansible-role-hosts
```

### Generate /etc/hosts with all IPv4 addresses of the host

```yaml
---
# role: ansible-role-hosts
# file: site.yml

- hosts: all
  become: true
  gather_facts: true
  vars:
    hosts_role_enabled: true
    hosts_ip_all: true
  roles:
    - role: ansible-role-hosts
```

## License and Author

- Author:: [jam82](https://github.com/jam82/)
- Copyright:: 2020, [jam82](https://github.com/jam82/)

Licensed under [MIT License](https://opensource.org/licenses/MIT).
See [LICENSE](https://github.com/jam82/ansible-role-hosts/blob/master/LICENSE) file in repository.
