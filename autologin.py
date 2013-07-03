#!/usr/bin/env python
#
# Logs in to dyndns so your account is kept active.
#

import random
import sys

import mechanize


SETTINGS = {
    'username': '',
    'password': ''
}

SEARCH_STR = '<span>Welcome&nbsp;<b>{0}</b></span>'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'
]


if __name__ == '__main__':
    if not SETTINGS['username'] or not SETTINGS['password']:
        sys.stderr.write("You need to configure the autologin.SETTINGS variable\n")
        sys.exit(-1)
    mech = mechanize.Browser()
    mech.set_handle_robots(False)
    mech.set_handle_redirect(True)
    mech.set_handle_referer(True)
    mech.addheaders = [('User-agent', random.choice(USER_AGENTS))]
    mech.open('https://account.dyn.com/')
    mech.select_form(nr=0)
    mech['username'] = SETTINGS['username']
    mech['password'] = SETTINGS['password']
    result = mech.submit().read()
    if SEARCH_STR.format(SETTINGS['username']) not in result:
        sys.stderr.write("Didn't find welcome message in response.\n")
        sys.stderr.write("Something might be wrong. Log in manually.\n")
        sys.exit(-1)
    else:
        print 'Logged in successfully.'
        sys.exit(0)
