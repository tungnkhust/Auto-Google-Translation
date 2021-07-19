import os
import json


def load_proxy(file_path, status_file=None):
    statuses = None
    if status_file:
        statuses = {}
        with open(status_file, 'r') as pf:
            proxy_status = pf.readlines()
            for line in proxy_status:
                tmp = line.split(': ')
                statuses[tmp[0]] = tmp[1].replace('\n', '')
    with open(file_path, 'r') as pf:
        lines = pf.readlines()
        proxy_address = [line.split(' ')[0] for line in lines]
        proxy_address_success = []
        if statuses:
            for proxy in proxy_address:
                ip = proxy.split(':')[0]
                if ip in statuses:
                    if statuses[ip] == 'success':
                        proxy_address_success.append(proxy)
        return proxy_address_success


def parse_string(text):
    """Replace the following characters in the text"""
    special_characters = (
            ("%", "%25"),
            (" ", "%20"),
            (",", "%2C"),
            ("?", "%3F"),
            ("\n", "%0A"),
            ('\"', "%22"),
            ("<", "%3C"),
            (">", "%3E"),
            ("#", "%23"),
            ("|", "%7C"),
            ("&", "%26"),
            ("=", "%3D"),
            ("@", "%40"),
            ("#", "%23"),
            ("$", "%24"),
            ("^", "%5E"),
            ("`", "%60"),
            ("+", "%2B"),
            ("\'", "%27"),
            ("{", "%7B"),
            ("}", "%7D"),
            ("[", "%5B"),
            ("]", "%5D"),
            ("/", "%2F"),
            ("\\", "%5C"),
            (":", "%3A"),
            (";", "%3B")
        )

    for pair in special_characters:
        text = text.replace(*pair)

    return text


def write_json(data, file_path, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as pf:
        json.dump(data, pf, ensure_ascii=False, indent=4)


def load_json(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as pf:
        data = json.load(pf)
        return data