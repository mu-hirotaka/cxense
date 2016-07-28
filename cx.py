#!/usr/bin/env python
"""\
Execute API requests.

Usage: cx.py <api path> <request object>

    Authentication is done by generating the appropriate header after reading the
    line 'authentication <username> <api key>' from ~/.cxrc.

    JSON will be seralized according to the default encoding, or ascii safe if
    in doubt.

    Stdin will be used if request object is "-". If no request object, the
    empty object "{}" is assumed.

Wiki references and documentation:
    API authentication: https://wiki.cxense.com/display/cust/API+authentication
    Requests and responses: https://wiki.cxense.com/display/cust/Requests+and+responses

Examples (for bash, please check the wiki pages for tips how to run this on Windows)

    Version:
        $ cx.py --version
        VERSION cx.py : '140331'
        
    Absolute path:
        $ cx.py https://api.cxense.com/public/date
        {
              "date": "2013-04-22T15:06:20.252Z"
        }

    Relative path, defaults to https://api.cxense.com unless apiserver is set in ~/.cxrc
        $ cx.py /public/date
        {
              "date": "2013-04-22T15:06:20.252Z"
        }

    POST request with non-empty request object:
        $ cx.py /site '{"siteId":"9222300742735526873"}'
        {
          "sites": [
            {
              "id": "9222300742735526873"
              "name": "Example site",
              "url": "http://www.example.com",
              "country": "US",
              "timeZone": "America/Los_Angeles",
            }
          ]
        }

    GET request with json parameter:
        $ cx.py /profile/content/fetch?json=%7B%22url%22%3A%22http%3A%2F%2Fwww.example.com%22%7D
        {
          "url": "http://www.example.com",
          "id": "0caaf24ab1a0c33440c06afe99df986365b0781f"
        }        
        
"""

'''
changelog:
    140331  pa: new --version flag
                support for GET requests documented https://wiki.cxense.com/display/cust/Requests+and+responses
                added simple doctest for execute()

'''

import os
import sys
import hmac
import json
import locale
import hashlib
import httplib
import datetime
import urlparse
import collections

#
# please update the version 
#
VERSION_TIMESTAMP = '140331'

# Default configuration.
username = None
secret = None
apiserver = 'https://api.cxense.com'

# Locate and autoload configuration from ~/.cxrc
rc = os.path.join(os.path.expanduser('~'), '.cxrc')
if os.path.exists(rc):
    for line in open(rc):
        fields = line.split()
        if fields[0] == 'authentication' and len(fields) == 3:
            username = fields[1]
            secret = fields[2]
        elif fields[0] == 'apiserver' and len(fields) == 2:
            apiserver = fields[1]

def getDate(connection):
    # If the computer's time can be trusted, the below condition can be changed to False
    if True:
        try:
            connection.request("GET", "/public/date")
            return json.load(connection.getresponse())['date']
        except:
            pass

    return datetime.datetime.utcnow().isoformat() + "Z"

def execute(url, obj, username=username, secret=secret):
    '''
    Doctest, call it 
        python -m doctest -v cx.py

    >>> execute(urlparse.urlparse('https://api.cxense.com/public/date'), None)[0]==200
    True
    
    >>> execute(urlparse.urlparse('https://api.cxense.com/profile/content/fetch'), json.loads('{"url":"http://www.example.com"}'))[0]==200
    True

    '''
    connection = (httplib.HTTPConnection if url.scheme == 'http' else httplib.HTTPSConnection)(url.netloc)
    try:
        date = getDate(connection)
        signature = hmac.new(secret, date, digestmod=hashlib.sha256).hexdigest()
        headers = {"X-cXense-Authentication": "username=%s date=%s hmac-sha256-hex=%s" % (username, date, signature)}
        headers["Content-Type"] = "application/json; charset=utf-8"
        if obj is None:
            # GET request
            connection.request("GET", url.path + ("?" + url.query if url.query else ""), headers=headers)
        else:
            # POST request with payload
            connection.request("POST", url.path + ("?" + url.query if url.query else ""), json.dumps(obj), headers=headers)
            
        response = connection.getresponse()
        return response.status, response.getheader('Content-Type', ''), response.read()

    except Exception, e:
        return e, 'application/json', {"error": str(e)}

    finally:
        connection.close()

if __name__ == "__main__":
    # print 'argv: ', repr(sys.argv) # DEBUG
    
    # if only two arguments are given, run it as GET \
    # instead of a POST request (which needs to have three arguments)
    IS_GET_REQUEST = len(sys.argv) == 2 

    # output the version number of this script
    if ('-v' in sys.argv) or ('--version' in sys.argv):
        print 'VERSION cx.py : %r\n' % VERSION_TIMESTAMP
        sys.exit()
        
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print 'VERSION cx.py: %r\n' % VERSION_TIMESTAMP
        print(__doc__)
        sys.exit(1)

    elif len(sys.argv) > 3:
        print("Too many arguments. Remember to quote the JSON.")
        sys.exit(1)

    if username is None or secret is None:
        print("Please add the line 'authentication <username> <api key>' to %s" % rc)
        sys.exit(3)

    if '@' not in username:
        print("Username is not an email address: %s" % username)
        sys.exit(4)

    if not secret.startswith('api&'):
        print("Invalid API key: %s" % secret)
        sys.exit(5)

    # Load data from argument or stdin, hopefully with correct encoding.
    obj = None # INIT
    try:
        if IS_GET_REQUEST:
            # GET request: early integrity check of optional json query parameter
            # if no json parameter exists (like for /public/date), surpass the test with "{}" as dummy instead
            json.loads(urlparse.parse_qs(urlparse.urlparse(sys.argv[-1]).query).get('json',["{}"])[-1])
            
        else:
            # POST request payload preparation
            data = sys.argv[2] if len(sys.argv) > 2 else None

            # Default to empty object.
            if data is None:
                obj = {}

            elif data == '-':
                obj = json.load(sys.stdin)

            else:
                obj = json.loads(unicode(data, sys.stdin.encoding or locale.getpreferredencoding()))
        
    except ValueError, e:
        print(json.dumps({"error": "Invalid JSON: %s" % e}))
        sys.exit(3)

    # Make sure piping works, which can have a undefined encoding.
    ensure_ascii = sys.stdout.encoding != 'UTF-8'

    # Default to apiserver, unless a full URL was given.
    path = sys.argv[1]
    if path.startswith('http'):
        url = urlparse.urlparse(path)
    else:
        url = urlparse.urlparse(urlparse.urljoin(apiserver, path))
        
    # Execute the API request and exit 0 only if it was successful.
    status, contentType, response = execute(url, obj, username, secret)
    if contentType.startswith('application/json'):
        print(json.dumps(json.loads(response, object_pairs_hook=collections.OrderedDict), indent=2, ensure_ascii=ensure_ascii))
    else:
        print response
    if status != 200:
        sys.exit(1)