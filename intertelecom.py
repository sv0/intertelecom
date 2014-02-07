#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = "Slavik Svyrydiuk"
__email__ = "svyrydiuk@gmail.com"
import re
import requests

LOGIN_URL = 'https://assa.intertelecom.ua/ru/login/'


def get_account_statistics(phone, password):
    # Log in assa.intertelecom.ua and return page response.content
    response = requests.post(
        LOGIN_URL,
        data={'phone': phone, 'pass': password, 'ref_link': '', 'js': '1'},
        timeout=30
    )

    current_session_traffic = float(
        re.search(
            r'<td>Трафик МБ</td>.*?(\d{1,4}\.\d{1,4}).*?</tr>',
            response.content,
            re.S
        ).group(1)
    )

    prepaid_traffic = sum([
        float(traf) for traf in re.findall(
            r'<td>пакетный трафик.*?(\d{1,5}\.\d{1,5}).*?</tr>',
            response.content,
            re.S
        )])

    balance = float(
        re.search(
            r'<td>Сальдо.*?(\d{1,5}\.\d{1,2}).*?</tr>',
            response.content, re.S
        ).group(1)
    )

    ip = re.search(
        r'<td>IP.*?(\b\d+(?:\.\d+){3}\b).*?</tr>', response.content, re.S
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

    account_statistics = get_account_statistics(args.user, args.password)
    values = []
    if args.trafic:
        values.append(str(int(account_statistics['available_trafic'])))
    if args.balance:
        values.append(str(account_statistics['balance']))

    print args.field_separator.join(values)
