
import re
from typing import Dict, List

REGEXP_PORT_ASSIGN = r'^(?:(?:\d{1,5}:)?\d{1,5}|:\d{1,5})/(?:tcp|udp)$'

# Input Format:
# [
#     '80:8080/tcp',
#     '123:123/udp'
#     '4040/tcp',
# ]
# Result Format:
# [
#     {
#         'cport': '80',
#         'hport': '8080',
#         'proto': 'tcp',
#     },
#     ...
# ]
def conv_ports2dict(data: List[str]) -> List[Dict[str,str]]:
    delim = ':'
    portlst = []
    for port_data in data:
        if not re.match(REGEXP_PORT_ASSIGN, port_data, flags=re.IGNORECASE):
            raise ValueError('Malformed port assignment.')

        cport,hport = None,port_data
        if delim in hport:
            cport,hport = hport.split(delim, 1)
            if not cport: cport = None
        hport,proto = hport.split('/', 1)
        portlst.append({ 'cport': cport, 'hport': hport, 'proto': proto })
    return portlst

# Input Format:
# [
#     {
#         'net.ipv6.conf.all.disable_ipv6': '0'
#     }
# ]
# Result Format:
# [
#     {
#         'name': 'net.ipv6.conf.all.disable_ipv6',
#         'value': '0'
#     }
# ]
def conv_sysctls2dict(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{ 'name': k, 'value': v } for item in data for k,v in item.items()]