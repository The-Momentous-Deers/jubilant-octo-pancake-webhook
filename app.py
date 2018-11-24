#!/usr/bin/env python
import os

from flask import Flask
from flask import request
from flask import make_response

import json, time, pprint
from urllib.request import Request, urlopen

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    res = req.get("queryResult")
    act = res.get("action")
    data = None
    if act == "bankbalance":
        print("Hello, Bank Balance PLS!")
        res = makeWebhookResult(RailsbankRequest().getBalance())
    else:
        res = makeWebhookResult("Sorry, Not sure what you mean")    
    return res

base_url = 'https://play.railsbank.com/'

# The next line contains get post and put helper functions, which should be replaced with a library of your choice in production code
custom_fetch = lambda method, relative_url, body=None: json.loads(urlopen(Request(base_url+relative_url, data=json.dumps(body).encode('utf8'), method=method, headers={'Content-Type': 'application/json', 'Authorization': 'API-Key ' + api_key, 'Accept': 'application/json'})).read().decode('utf-8')); post = lambda url, body=None: custom_fetch("POST", url, body); get = lambda url: custom_fetch("GET", url); put = lambda url, body=None: custom_fetch("PUT", url, body)

# Make sure to replace `***EXAMPLE KEY***` in the next line with your api key of form <key_id>#<key_secret>
api_key = os.environ.get('API_KEY', None)

class RailsbankRequest:

    ledger_id = "5bf951a0-8c73-437c-ae59-ac60a0f9847e"

    def __init__(self):
        response = get('v1/customer/me')
        pprint.pprint(response)
        self.customer_id = response['customer_id']

    def getBalance(self):
        response = get('v1/customer/ledgers/' + str(self.ledger_id))
        return "Your balance is " + str(response['amount']) + " pounds."


def makeWebhookResult(speech):
    return {
        "fulfillmentText": speech,
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % (port))

    app.run(debug=False, port=port, host='0.0.0.0')
