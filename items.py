pkg_apt = {
    "resolvconf": {
        'installed': False,
    },
}

actions = {
    'routes-enforce': {
        'command': "/usr/local/sbin/routes-enforce",
        'expected_return_code': None,
        'triggered': True,
    },
}

files = {
    "/etc/network/interfaces": {
        'source': "etc/network/interfaces",
        'content_type': 'mako',
        'mode': "0644",
        'owner': "root",
        'group': "root",
    },
    "/etc/resolv.conf": {
        'content_type': 'mako',
        'mode': "0644",
        'owner': "root",
        'group': "root",
        'source': "etc/resolv.conf",
    },
    "/usr/local/sbin/routes-enforce": {
        'source': "usr/local/sbin/routes-enforce",
        'content_type': 'mako',
        'mode': "0755",
        'owner': "root",
        'group': "root",
        'needed_by': ['action:routes-enforce'],
    },
    "/etc/network/if-up.d/restore-routing": {
        'source': "etc/network/if-up.d/restore-routing",
        'content_type': 'text',
        'mode': "0755",
        'owner': "root",
        'group': "root",
        'triggers': ['action:routes-enforce'],
    }
}

