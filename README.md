# ansible-role-hosts

**Ansible role for configuring the `/etc/hosts` file.**

## Supported Platforms

- Alpine
- Amazonlinux
- Archlinux
- CentOS
- Debian
- Fedora
- Oraclelinux
- Suse
- Ubuntu

## Requirements

Ansible 2.8 or higher.

## Variables

Variables and defaults for this role in defaults/main.yml:

```yaml
---
# role: ansible-role-hosts
# file: defaults/main.yml

# The role is disabled by default, so you do not get in trouble.
# Checked in tasks/main.yml which includes tasks.yml if enabled.
hosts_enabled: False

# Backup the hosts file when applying template
hosts_backup: True

# Determine how the targeted host(s) is added to /etc/hosts
# hosts_ip_all:
#   True  = generates entries for all IPs in ansible_all_ipvX_addresses
#           with ansible_fqdn and ansible_hostname
#   False = generates single entry for value of key "address"
#           with ansible_fqdn and ansible_hostname dependant on static setting
hosts_ip_all: False
# hosts_ip_static:
#   True  = use address defined in key "address"
#   False = use 127.0.1.1 if IP obtained via dhcp.
#           If IP is not obtained by dhcp the value of key "address" is used.
hosts_ip_static: False
# hosts_ip_static:
#   IP address to use, when "hosts_ip_all: False", and
#   "hosts_ip_static: True" or "static: False" and IP not obtained via dhcp
#   If "static: False" and IP was obtained via dhcp then 127.0.1.1 is used
hosts_ip_address: "{{ ansible_default_ipv4.address }}"

# Additional entries in the hosts file
# hosts_entries:
#   - name: test.blabla.tld
#     aliases:
#       - test
#       - test1.blabla.tld
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

- hosts: hosts_systems
  become: True
  vars:
    hosts_enabled: True
  roles:
    - role: ansible-role-hosts
```

### Force static IP in /etc/hosts even if obtained by dhcp

```yaml
---
# role: ansible-role-hosts
# file: site.yml

- hosts: hosts_systems
  become: True
  vars:
    hosts_enabled: True
    hosts_ip_static: True
  roles:
    - role: ansible-role-hosts
```

### Generate /etc/hosts with all IPv4 addresses of the host

```yaml
---
# role: ansible-role-hosts
# file: site.yml

- hosts: hosts_systems
  become: True
  vars:
    hosts_enabled: True
    hosts_ip_all: True
  roles:
    - role: ansible-role-hosts
```

## License and Author

- Author:: [jam82](https://github.com/jam82/)
- Copyright:: 2020, [jam82](https://github.com/jam82/)

Licensed under [MIT License](https://opensource.org/licenses/MIT).
See [LICENSE](https://github.com/jam82/ansible-role-hosts/blob/master/LICENSE) file in repository.
