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
    outcontext = res.get("outputContexts")
    session = req.get("session")
    print(outcontext)

    interface.enduser_id = ""
    interface.ledger_id = ""

    if act != "auth":
        # Get the ID
        try:
            auth = False
            contextpath = "projects/jubilant-octo-pancake-96395/agent/sessions/"+str(session)+"/contexts/id"
            print(contextpath)
            context = next(item for item in contexts if item["name"] == contextpath
            interface.enduser_id = outcontext[0]['parameters']['enduser_id']
            interface.ledger_id = outcontext[0]['parameters']['ledger_id']
            print("Authenticated")
        except:
            act = "FAILED"
            res = makeWebhookResult("You are not authenticated. Log in using the authenticate command.")
            return res
    
    data = None
    if act == "bankbalance":
        print("Hello, Bank Balance PLS!")
        res = makeWebhookResult("Your balance is " + str(interface.getBalance()) + " pounds")
    elif act == "beneficiary":
        print("Hello, Add a Beneficiary PLS!")
        res = makeWebhookResult(interface.makeBeneficiary(parameters.get("IBAN"), parameters.get("BIC"), parameters.get("given-name")))
    elif act == "auth":
        print("Authenticating")
        name = parameters.get("given-name") + " " + parameters.get("last-name") 
        dbmanagerResponse = dbmanager.validatePassword(name, parameters.get("password"))
        outputcontext = [
            {
                "name": session + "/contexts/id", 
                "lifespanCount": 5, 
                "parameters": {
                    "enduser_id": dbmanagerResponse['id'],
                    "ledger_id": dbmanagerResponse['ledger_id']
                }
            }
        ]
        res = makeWebhookResult(dbmanagerResponse['data']['msg'], outputcontext)
    elif act == "transaction":
        print("Transaction")
    else:
        res = makeWebhookResult("Sorry, Not sure what you mean")
     
    return res

# Make sure to replace `***EXAMPLE KEY***` in the next line with your api key of form <key_id>#<key_secret>
api_key = os.environ.get('API_KEY', None)

def makeWebhookResult(speech, context=None):
    #print("Speech: " + speech)
    #print("Context: " + str(context))
    return {
        "fulfillmentText": speech,
        "outputContexts": context
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % (port))

    app.run(debug=False, port=port, host='0.0.0.0')
