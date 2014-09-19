#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = "Slavik Svyrydiuk"
__email__ = "svyrydiuk@gmail.com"
import re
import urllib
import urllib2

LOGIN_URL = 'https://assa.intertelecom.ua/ru/login/'


def get_account_home_page(phone, password):
    """
    Log into Intertelecom ASSA and return home page's HTML
    """
    login_data = urllib.urlencode({
        'phone': phone,
        'pass': password,
        'ref_link': '',
        'js': '1'
    })
    req = urllib2.Request(LOGIN_URL, login_data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    r = opener.open(req)
    return r.read()


def parse_account_statistics(html):
    current_session_traffic = float(
        re.search(
            r'<td>Трафик МБ</td>.*?(\d{1,4}\.\d{1,4}).*?</tr>',
            html,
            re.S
        ).group(1)
    )

    prepaid_traffic = sum([
        float(traf) for traf in re.findall(
            r'<td>пакетный трафик.*?(\d{1,5}\.\d{1,5}).*?</tr>',
            html,
            re.S
        )])

    balance = float(
        re.search(
            r'<td>Сальдо.*?(\d{1,5}\.\d{1,2}).*?</tr>',
            html, re.S
        ).group(1)
    )

    ip = re.search(
        r'<td>IP.*?(\b\d+(?:\.\d+){3}\b).*?</tr>', html, re.S
    ).group(1)

    return {
        'current_session_traffic': current_session_traffic,
        'prepaid_traffic': prepaid_traffic,
        'available_trafic': prepaid_traffic - current_session_traffic,
        'balance': balance,
        'ip': ip,
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Get the trafic and balance statistics "
                    "of Intertelecom CDMA provider"
    )
    parser.add_argument(
        "-u", "--user",
        required=True,
        help="Username(phone number) to log in assa.intertelecom.ua"
    )
    parser.add_argument(
        "-p", "--password",
        required=True,
        help="Password"
    )
    parser.add_argument(
        "-t", "--trafic",
        help="Echo the available trafic amount",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "-b", "--balance",
        help="Echo the account balance",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f", "--field_separator",
        help="Field separator",
        default=':',
    )
    args = parser.parse_args()

    page_html = get_account_home_page(args.user, args.password)
    stat = parse_account_statistics(page_html)

    values = []
    if args.trafic:
        values.append(str(int(stat['available_trafic'])))
    if args.balance:
        values.append(str(stat['balance']))

    print args.field_separator.join(values)
