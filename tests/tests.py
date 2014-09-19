#!/usr/bin/env python
#-*- coding: utf-8 -*-
from os.path import realpath, dirname, join
import unittest
from intertelecom import parse_account_statistics


class IntertelecomTestCase(unittest.TestCase):
    def test_parse_account_statistics(self):
        html_filename = join(
            dirname(realpath(__file__)),
            'test-assa-intertelecom.html'
        )
        stat = parse_account_statistics(open(html_filename).read())
        self.assertEqual(stat['current_session_traffic'], 17.353)
        self.assertEqual(stat['prepaid_traffic'], 1152.9121)
        self.assertEqual(stat['balance'], 0.39)
        self.assertEqual(stat['ip'], '37.19.153.11')


if __name__ == '__main__':
    unittest.main()
