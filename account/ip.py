import socket

from django.conf import settings

# Search for the real IP address in the following order
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For
# X-Forwarded-For: <client>, <proxy1>, <proxy2>
# Configurable via settings.py
IPWARE_META_PRECEDENCE_ORDER = getattr(
    settings,
    "IPWARE_META_PRECEDENCE_ORDER",
    (
        "HTTP_X_FORWARDED_FOR",
        "X_FORWARDED_FOR",
        "HTTP_CLIENT_IP",
        "HTTP_X_REAL_IP",
        "HTTP_X_FORWARDED",
        "HTTP_X_CLUSTER_CLIENT_IP",
        "HTTP_FORWARDED_FOR",
        "HTTP_FORWARDED",
        "HTTP_VIA",
        "REMOTE_ADDR",
    ),
)

# Private IP addresses
# http://en.wikipedia.org/wiki/List_of_assigned_/8_IPv4_address_blocks
# https://en.wikipedia.org/wiki/Reserved_IP_addresses
# https://www.ietf.org/rfc/rfc1112.txt (IPv4 multicast)
# http://www.ietf.org/rfc/rfc3330.txt (IPv4)
# http://www.ietf.org/rfc/rfc5156.txt (IPv6)
# https://www.ietf.org/rfc/rfc6890.txt
# Regex would be ideal here, but this is keeping it simple
# Configurable via settings.py
IPWARE_PRIVATE_IP_PREFIX = getattr(
    settings,
    "IPWARE_PRIVATE_IP_PREFIX",
    (
        "0.",  # messages to software
        "10.",  # class A private block
        "100.64.",
        "100.65.",
        "100.66.",
        "100.67.",
        "100.68.",
        "100.69.",
        "100.70.",
        "100.71.",
        "100.72.",
        "100.73.",
        "100.74.",
        "100.75.",
        "100.76.",
        "100.77.",
        "100.78.",
        "100.79.",
        "100.80.",
        "100.81.",
        "100.82.",
        "100.83.",
        "100.84.",
        "100.85.",
        "100.86.",
        "100.87.",
        "100.88.",
        "100.89.",
        "100.90.",
        "100.91.",
        "100.92.",
        "100.93.",
        "100.94.",
        "100.95.",
        "100.96.",
        "100.97.",
        "100.98.",
        "100.99.",
        "100.100.",
        "100.101.",
        "100.102.",
        "100.103.",
        "100.104.",
        "100.105.",
        "100.106.",
        "100.107.",
        "100.108.",
        "100.109.",
        "100.110.",
        "100.111.",
        "100.112.",
        "100.113.",
        "100.114.",
        "100.115.",
        "100.116.",
        "100.117.",
        "100.118.",
        "100.119.",
        "100.120.",
        "100.121.",
        "100.122.",
        "100.123.",
        "100.124.",
        "100.125.",
        "100.126.",
        "100.127.",  # carrier-grade NAT
        "169.254.",  # link-local block
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31.",  # class B private blocks
        "192.0.0.",  # reserved for IANA special purpose address registry
        "192.0.2.",  # reserved for documentation and example code
        "192.168.",  # class C private block
        "198.18.",
        "198.19.",  # reserved for inter-network communications between two separate subnets
        "198.51.100.",  # reserved for documentation and example code
        "203.0.113.",  # reserved for documentation and example code
        "224.",
        "225.",
        "226.",
        "227.",
        "228.",
        "229.",
        "230.",
        "231.",
        "232.",
        "233.",
        "234.",
        "235.",
        "236.",
        "237.",
        "238.",
        "239.",  # multicast
        "240.",
        "241.",
        "242.",
        "243.",
        "244.",
        "245.",
        "246.",
        "247.",
        "248.",
        "249.",
        "250.",
        "251.",
        "252.",
        "253.",
        "254.",
        "255.",  # reserved
    )
    + (
        "::",  # Unspecified address
        "::ffff:",
        "2001:10:",
        "2001:20:" "2001::",  # messages to software  # TEREDO
        "2001:2::",  # benchmarking
        "2001:db8:",  # reserved for documentation and example code
        "fc00:",  # IPv6 private block
        "fe80:",  # link-local unicast
        "ff00:",  # IPv6 multicast
    ),
)

IPWARE_LOOPBACK_PREFIX = (
    "127.",  # IPv4 loopback device (Host)
    "::1",  # IPv6 loopback device (Host)
)

IPWARE_NON_PUBLIC_IP_PREFIX = IPWARE_PRIVATE_IP_PREFIX + IPWARE_LOOPBACK_PREFIX


def cleanup_ip(ip):
    """
    Given ip address string, it cleans it up
    """
    ip = ip.strip().lower()
    if ip.startswith("::ffff:"):
        return ip.replace("::ffff:", "")
    return ip


def is_valid_ipv4(ip_str):
    """
    Check the validity of an IPv4 address
    """
    try:
        socket.inet_pton(socket.AF_INET, ip_str)
    except AttributeError:  # pragma: no cover
        try:  # Fall-back on legacy API or False
            socket.inet_aton(ip_str)
        except (AttributeError, socket.error):
            return False
        return ip_str.count(".") == 3
    except socket.error:
        return False
    return True


def is_valid_ipv6(ip_str):
    """
    Check the validity of an IPv6 address
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
    except socket.error:
        return False
    return True


def is_valid_ip(ip_str):
    """
    Check the validity of an IP address
    """
    return is_valid_ipv4(ip_str) or is_valid_ipv6(ip_str)


def is_private_ip(ip_str):
    """
    Returns true of ip_str is private & not routable, else return false
    """
    return ip_str.startswith(IPWARE_NON_PUBLIC_IP_PREFIX)


def is_public_ip(ip_str):
    """
    Returns true of ip_str is public & routable, else return false
    """
    return not is_private_ip(ip_str)


def is_loopback_ip(ip_str):
    """
    Returns true of ip_str is public & routable, else return false
    """
    return ip_str.startswith(IPWARE_LOOPBACK_PREFIX)


def get_request_meta(request, key):
    """
    Given a key, it returns a cleaned up version of the value from request.META, or None
    """
    value = request.META.get(key, request.META.get(key.replace("_", "-"), "")).strip()
    if value == "":
        return None
    return value


def get_ips_from_string(ip_str):
    """
    Given a string, it returns a list of one or more valid IP addresses
    """
    ip_list = []

    for ip in ip_str.split(","):
        clean_ip = ip.strip().lower()
        if clean_ip:
            ip_list.append(clean_ip)

    ip_count = len(ip_list)
    if ip_count > 0:
        if is_valid_ip(ip_list[0]) and is_valid_ip(ip_list[-1]):
            return ip_list, ip_count

    return [], 0


def get_ip_info(ip_str):
    """
    Given a string, it returns a tuple of (IP, Routable).
    """
    ip = None
    is_routable_ip = False
    clean_ip = cleanup_ip(ip_str)
    if is_valid_ip(clean_ip):
        ip = clean_ip
        is_routable_ip = is_public_ip(ip)
    return ip, is_routable_ip


def get_best_ip(last_ip, next_ip):
    """
    Given two IP addresses, it returns the the best match ip.
    Order of precedence is (Public, Private, Loopback, None)
    Right-most IP is returned
    """
    if last_ip is None:
        return next_ip
    if is_public_ip(last_ip) and not is_public_ip(next_ip):
        return last_ip
    if is_private_ip(last_ip) and is_loopback_ip(next_ip):
        return last_ip
    return next_ip


def get_client_ip(
    request,
    proxy_order="left-most",
    proxy_count=None,
    proxy_trusted_ips=None,
    request_header_order=None,
):
    client_ip = None
    routable = False

    if proxy_count is None:
        proxy_count = -1

    if proxy_trusted_ips is None:
        proxy_trusted_ips = []

    if request_header_order is None:
        request_header_order = IPWARE_META_PRECEDENCE_ORDER

    for key in request_header_order:
        value = get_request_meta(request, key)
        if value:
            ips, ip_count = get_ips_from_string(value)

            if ip_count < 1:
                # we are expecting at least one IP address to process
                continue

            if proxy_count == 0 and ip_count > 1:
                # we are not expecting requests via any proxies
                continue

            if proxy_count > 0 and proxy_count != ip_count - 1:
                # we are expecting requests via `proxy_count` number of proxies
                continue

            if proxy_trusted_ips and ip_count < 2:
                # we are expecting requests via at least one trusted proxy
                continue

            if proxy_order == "right-most" and ip_count > 1:
                # we are expecting requests via proxies to be custom as per `<proxy2>, <proxy1>, <client>`
                ips.reverse()

            if proxy_trusted_ips:
                for proxy in proxy_trusted_ips:
                    # right most proxy is the most reliable proxy that talks to the django server
                    if ips[-1].startswith(proxy):
                        client_ip, routable = get_ip_info(ips[0])
                        if client_ip and routable:
                            return client_ip, routable
            else:
                client_ip, routable = get_ip_info(get_best_ip(client_ip, ips[0]))
                if client_ip and routable:
                    return client_ip, routable

    return client_ip, routable
