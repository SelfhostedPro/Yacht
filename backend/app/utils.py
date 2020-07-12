import re

REGEXP_PORT_ASSIGN = r'^(?:(?:\d{1,5}\:)?\d{1,5})|\:d{1,5}/(?:tcp|udp)$'

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
def conv_ports2dict(data):
    if not all(isinstance(x, str) for x in data):
        raise TypeError('Expected list or str types.')
    if not all(re.match(REGEXP_PORT_ASSIGN, x, flags=re.IGNORECASE) for x in data):
        raise ValueError('Malformed port assignment.')

    delim = ':'
    portlst = []
    for port_data in data:
        hport, cport = None,port_data
        if delim in cport:
            hport,cport = cport.split(delim, 1)
            if not hport: hport = None
        cport,proto = cport.split('/', 1)
        portlst.append({ 'hport': hport, 'cport': cport, 'proto': proto })
    return portlst