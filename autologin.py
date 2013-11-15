#!/usr/bin/env python2
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

    # find first form that has id starting with 'login'
    login_form = None
    for form in mech.forms():
        # DynDNS used dynamic names for login form like 'login142', 'login189', ...
        id = form.attrs['id']
        if id.startswith('login'):
            login_form = form
            break

    if not login_form:
        sys.stderr.write('Could not find login form. Maybe DynDNS changed site.')
        sys.exit(-1)

    # Set focus on form
    mech.form = login_form
    mech['username'] = USERNAME
    mech['password'] = PASSWORD
    result = mech.submit().read()
    if SEARCH_STR.format(USERNAME) not in result:
        sys.stderr.write("Didn't find welcome message in response.\n")
        sys.stderr.write("Something might be wrong. Log in manually.\n")
        mech.close()
        sys.exit(-1)
    else:
        print 'Logged in successfully.'
        mech.close()
        sys.exit(0)
