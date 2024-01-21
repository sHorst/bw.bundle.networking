import ipaddress

defaults = {}
if node.has_bundle("apt"):
    defaults = {
        'apt': {
            'packages': {
                'resolvconf': {'installed': True},
            }
        }
    }


def _prefix_length_ipv4(netmask):
    binary_str = ""
    for octet in netmask.split("."):
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip("0")))


def _network_address_ipv4(ip, netmask):
    return ".".join([
        str(int(ip.split(".")[x]) & int(netmask.split(".")[x]))
        for x in range(0, 4)
    ])


@metadata_reactor
def rewrite_ip_addresses_with_prefix(metadata):
    interfaces = {}
    for interface_name, interface_config in metadata.get('interfaces', {}).items():
        ip_addresses_prefix = []
        for ip in interface_config.get("ip_addresses", []):
            if len(ip.split("/")) == 2:
                ip_addresses_prefix += [str(ip)]
            else:
                ip_addresses_prefix += [str(
                    ipaddress.IPv4Interface(f"{ip}/{interface_config.get('netmask', '255.255.255.0')}").with_prefixlen)]

        interfaces = {
            interface_name: {
                'ip_addresses_prefix': ip_addresses_prefix
            }
        } | interfaces

    return {
        'interfaces': interfaces
    }

@metadata_reactor
def metaproc_add_cidr(metadata):
    interfaces = {}
    """
    This metadata processor will add a CIDR-style network attribute to
    all configured interfaces. E.g. for

    node.metadata['interfaces']['eth0']['ip_addresses'] == ["10.1.2.3"]
    node.metadata['interfaces']['eth0']['netmask'] == "255.255.255.0"

    this will add

    node.metadata['interfaces']['eth0']['net_cidr'] == "10.1.2.0/24"
    """
    for interface_name, interface_config in metadata.get('interfaces', {}).items():
        if 'ip_addresses' not in interface_config:
            continue

        interfaces = {
            interface_name: {
                'net_cidr': "{}/{}".format(
                    _network_address_ipv4(
                        interface_config['ip_addresses'][0],
                        interface_config.get('netmask', "255.255.255.0"),
                    ),
                    _prefix_length_ipv4(
                        interface_config.get('netmask', "255.255.255.0"),
                    ),
                )
            }
        }

    return {
        'interfaces': interfaces
    }
