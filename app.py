#!/usr/bin/env python
import os

from flask import Flask
from flask import request
from flask import make_response

import json, time, pprint
from urllib.request import Request, urlopen

from railsbankinterface.railsbankinterface import RailsbankRequest
from db_interface import *


# Flask app should start in global layout
app = Flask(__name__)
interface = RailsbankRequest()
dbmanager = DbManager()

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
    parameters = res.get("parameters")
    data = None
    if act == "bankbalance":
        print("Hello, Bank Balance PLS!")
        res = makeWebhookResult(interface.getBalance())
    elif act == "beneficiary":
        print("Hello, Add a Beneficiary PLS!")
        res = makeWebhookResult(interface.makeBeneficiary(parameters.get("IBAN"), parameters.get("BIC"), parameters.get("given-name")))
    elif act == "auth":
        print("Authenticating")
        name = parameters.get("given-name") + " " + parameters.get("last-name") 
        dbmanagerResponse = dbmanager.validatePassword(name, parameters.get("password"))
        res = makeWebhookResult(dbmanagerResponse['data']['msg'], {"userStorage": dbmanagerResponse['id']})
    elif act == "transaction":
        print("Transaction")
        
    else:
        res = makeWebhookResult("Sorry, Not sure what you mean")    
    return res

# Make sure to replace `***EXAMPLE KEY***` in the next line with your api key of form <key_id>#<key_secret>
api_key = os.environ.get('API_KEY', None)

def makeWebhookResult(speech, data):

    return {
        "fulfillmentText": speech,
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % (port))

    app.run(debug=False, port=port, host='0.0.0.0')
