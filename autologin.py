#!/usr/bin/env python
#
# Logs in to dyndns so your account is kept active.
#

import random
import sys

import mechanize

try:
    from settings import USERNAME, PASSWORD
except ImportError:
    print "You need to create a settings.py file with the following content:"
    print "USERNAME = 'my_username_here'"
    print "PASSWORD = 'my_password_here'"
    print "\n"
    sys.exit(-1)


SEARCH_STR = '<span>Welcome&nbsp;<b>{0}</b></span>'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'
]


if __name__ == '__main__':
    mech = mechanize.Browser()
    mech.set_handle_robots(False)
    mech.set_handle_redirect(True)
    mech.set_handle_referer(True)
    mech.addheaders = [('User-agent', random.choice(USER_AGENTS))]
    mech.open('https://account.dyn.com/')
    mech.select_form(nr=0)
    mech['username'] = USERNAME
    mech['password'] = PASSWORD
    result = mech.submit().read()
    if SEARCH_STR.format(USERNAME) not in result:
        sys.stderr.write("Didn't find welcome message in response.\n")
        sys.stderr.write("Something might be wrong. Log in manually.\n")
        sys.exit(-1)
    else:
        print 'Logged in successfully.'
        sys.exit(0)
