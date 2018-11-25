import json, time, pprint
from urllib.request import Request, urlopen
import urllib.error

base_url = 'https://playlive.railsbank.com/'

# The next line contains get post and put helper functions, which should be replaced with a library of your choice in production code
custom_fetch = lambda method, relative_url, body=None: json.loads(urlopen(Request(base_url+relative_url, data=json.dumps(body).encode('utf8'), method=method, headers={'Content-Type': 'application/json', 'Authorization': 'API-Key ' + api_key, 'Accept': 'application/json'})).read().decode('utf-8')); post = lambda url, body=None: custom_fetch("POST", url, body); get = lambda url: custom_fetch("GET", url); put = lambda url, body=None: custom_fetch("PUT", url, body)

# Make sure to replace `***EXAMPLE KEY***` in the next line with your api key of form <key_id>#<key_secret>
#api_key = 'ayzmam4ta3uu3n1quuvq8u0m3kcl4vnx#6sipzuhpoemrwr1kvcgxe0dtjnneryjg0lngqbq9l777j89jsv8th28pferkt43g' #play key
api_key = 'nkjzi7r487m0tvz1utveuvr1guy4pkhg#gn7xy31t2wem2awxk4w4552qmn3jy4z4rgqtssz3w9ihjm1t1dstf3kyyutlte28' #play live key



class RailsbankRequest:

    def __init__(self):
        # This needs to fetch the relevant data from the database
        # data includes, ledgerID, benifactoryID, enduserID?
        response = get('v1/customer/me')
        # pprint.pprint(response)
        self.customer_id = response['customer_id']
        self.enduser_id = '5bf9f0b5-4962-4e88-a83a-2360df15fe67'#This allows us to reuse endusers
        pprint.pprint("self.customer_id = " + self.customer_id)
        pprint.pprint("self.enduser_id = " + self.enduser_id)

    def makeEnduser(self):
        response = post(
            'v1/customer/endusers', {
                'person': {
                    'name': 'Jane',
                    'email': 'jane@email.com',
                    'address': {
                        'address_iso_country' : 'GB',
                        'address_postal_code' : 'POS COD',
                        'address_number' : '420'
                    }
                }
            })

        #pprint.pprint("\nPrinting post enduser response\n")
        #pprint.pprint(response)
        #self.enduser_id = response['enduser_id']

        """
        Enduser is not ready immediately because of ongoing validity checks.
        """
        #response = get('v1/customer/endusers/' + str(self.enduser_id) + '/wait')
        #pprint.pprint(response)


    #def fetchEnduser(self):
    #    response = get('v1/customer/endusers/' + self.enduser_id)




    def makeLedger(self):
        '''
        Creating ledger assigned to our enduser and assigning iban to it.
        '''
        response = post(
            'v1/customer/ledgers', {
	           "holder_id": self.customer_id,
               "partner_product": "PayrNet-GBP-1",
	           "asset_class": "currency",
	           "asset_type": "gbp",
               "ledger_type": "ledger-type-omnibus",
               "ledger_who_owns_assets": "ledger-assets-owned-by-me",
               "ledger_primary_use_types": ["ledger-primary-use-types-payments"],
               "ledger_t_and_cs_country_of_jurisdiction": "GBR"
        })
        # pprint.pprint(response)
        self.ledger_id = response['ledger_id']
        # pprint.pprint(response)

        pprint.pprint(response)
        ledger_id = response['ledger_id']
        time.sleep(10)
        response = get('v1/customer/ledgers/' + str(ledger_id))
        pprint.pprint(response)
        #response = post('v1/customer/ledgers/' + str(ledger_id) + '/assign-iban')
        #pprint.pprint(response)
        response = get('v1/customer/ledgers/' + str(ledger_id) + '/wait')
        pprint.pprint(response)
        uk_sort_code = response['uk_sort_code']
        uk_account_number = response['uk_account_number']
        '''
        Crediting the ledger with 10 euro.
        '''
        #response = post('dev/customer/transactions/receive', {
        #    'iban': iban,
        #    'bic-swift': bic,
        #    'amount': 10
        #})
        #transaction_receive_id = response['transaction_id']
        '''
        We need to wait for the transaction to be approved.
        '''
        #time.sleep(10)
        #response = get('v1/customer/transactions/' + str(transaction_receive_id))
        #pprint.pprint(response)



    def fetchLedger(self):
        response = get('v1/customer/endusers/'+self.enduser_id)
        pprint.pprint("Printing Fetch Ledger Response")
        pprint.pprint(response)
        ledgerlist=response["ledgers"]
        self.ledger_id = ledgerlist[0]['ledger_id']
        #self.holder_id = response['holder_id']
        #pprint.pprint("All holder_id = " + self.holder_id)
        pprint.pprint("All customer_id = " + self.customer_id)
        pprint.pprint("All ledgers are")
        pprint.pprint(ledgerlist)
        pprint.pprint("self.ledger_id = " + self.ledger_id)



    def showLedger(self):
        response = get('v1/customer/ledgers/' + self.ledger_id + '/wait')
        pprint.pprint("PRINTING LEDGER INFO")
        pprint.pprint(response)



    def requestcard(self):
        '''#Dont uncomment this code as we have a limit on the number of endusers
        #creating a card holding end user
        response = post(
        'v1/customer/endusers',{
	        "person": {
            "name": "John Smith",
            'address': {
                'address_iso_country': 'GB',
                'address_postal_code': "PO5 1OD",
                'address_number': "420"
                }
            }
        }) #return enduser_id: something
        pprint.pprint(response)
        self.enduser_id = response["enduser_id"]
        '''#Dont uncomment this code as we have a limit on the number of endusers
        #pprint.pprint(self.enduser_id)
        #finshed creating a card holding end user
        #Issueing an enduser with a EUR ledger
        #response = post(
        #'v1/customer/ledgers',{
        #    "holder_id": self.enduser_id,
	    #    "partner_product": "PayrNet-GBP-1",
	    #    "asset_class": "currency",
	    #    "asset_type": "gbp",
        #    "ledger_type": "ledger-type-single-user",
        #    "ledger_who_owns_assets": "ledger-assets-owned-by-me",
        #    "ledger_primary_use_types": ["ledger-primary-use-types-payments"],
        #    "ledger_t_and_cs_country_of_jurisdiction": "GBR"
        #    })#returns ledger_id in a dictionary
        #self.ledger_id = response['ledger_id']
        pprint.pprint("\nGonna print the first ledger ID\n")
        pprint.pprint(self.ledger_id)
        #Finished issueing an enduser with a EUR ledger
        #issueing the card
        pprint.pprint("self.ledger_id = ")
        pprint.pprint(self.ledger_id)
        pprint.pprint("\nISSUEING CARD\n")
        response = post(
            'v1/customer/cards',  {
                "ledger_id": self.ledger_id,
                "partner_product": "Railsbank-Debit-Card-1",
                "card_programme": "openbankhack18"
                })#returns "card_id": {card id}
        self.card_id = response["card_id"]
        pprint.pprint('self.card_id = ')
        pprint.pprint(self.card_id)
        #Make sure that you have rails-bank debit card bought
        #activating cards
        pprint.pprint('v1/customer/cards/'+self.card_id+'/activate')
        #response = post('v1/customer/cards/'+self.card_id+'/activate')
        #post('v1/customer/cards/'+self.card_id+'/activate')

        get('v1/customer/cards/'+self.card_id)
        pprint.pprint("Getting URL")
        pprint.pprint(response)
        response = get('v1/customer/cards/' + self.card_id)



    def fetchCard(self):
        response = get('v1/customer/cards')
        pprint.pprint(response)
        self.card_id = response[0]['card_id']
        self.card_program = response[0]['card_programme']
        pprint.pprint('self.card_id = '+self.card_id)



    def activateCard(self):
        response = post('v1/customer/cards/'+self.card+'/activate')
        pprint.pprint(response["card_status"])



    def getBalance(self):
        response = get('v1/customer/ledgers/' + str(self.ledger_id))
        pprint.pprint(response["amount"])
        return response["amount"]



    def makeBeneficiary(self):
        '''
        Creating beneficiary for our enduser.
        '''
        response = post(
        {
            "uk_account_number": "12345678",
            "uk_sort_code": "123456",
            "holder_id": self.enduser_id,
            "asset_class": "currency",
            "asset_type": "gbp",
            "person": {
                "country_of_residence": ["GB"],
                "address":{
                    "address_refinement": "Apartment 77",
                    "address_number": "42",
                    "address_street": "London Road",
                    "address_city": "London",
                    "address_region": "Greater London",
                    "address_postal_code": "SW1 4AQ",
                    "address_iso_country": "GBR"
                },
                "date_onboarded": "2015-11-21",
                "email": "harrison@example.net",
                "name": "Harrison Smith",
                "telephone": "+44 22 626 2626",
                "date_of_birth": "1970-11-05",
                "nationality": ["British"]
            },
            "beneficiary_meta": {
                "foo": "baa",
                "our_salesforce_reference": "http://na1.salesforce.com/5003000000D8cuI"
            }
        })

        pprint.pprint(response)
        self.beneficiary_id = response['beneficiary_id']

        '''
        Beneficiary is not ready immediately because of ongoing validity checks.
        '''
        response = get('v1/customer/beneficiaries/' + str(self.beneficiary_id) + '/wait')

    def fetchBeneficiary(self):
        response = get('v1/customer/beneficiaries/')
        #self.beneficiaries = response['beneficiaries']
        pprint.pprint("Beneficiary list = ")
        pprint.pprint(response)
        beneficiaries = response
        #self.beneficiary = response[0]



    def makePayment(self):
        '''
        Creating 2 euro transaction from the ledger to the beneficiary.
        '''
        response = post(
            'v1/customer/transactions', {
                'ledger_from_id': self.ledger_id,
                'beneficiary_id': self.beneficiary_id,
                'payment_type': 'payment-type-EU-SEPA-Step2',
                'amount': '2'
                })
        pprint.pprint(response)
        transaction_id = response['transaction_id']

        '''
        We need to wait for the transaction to be approved.
        '''
        time.sleep(10)
        response = get('v1/customer/transactions/' + str(transaction_id))
        pprint.pprint(response)



    def addMoney(self):
        response = post(
            'dev/customer/transactions/receive', {
                'amount': 10,
                'uk_account_number': '12345678',
                'uk_sort_code': '123434'
            })
        '''
        We need to wait for the transaction to be approved.
        '''
        transaction_receive_id = response['transaction_id']
        time.sleep(10)
        response = get('v1/customer/transactions/' + str(transaction_receive_id))
        pprint.pprint(response)



if __name__ == "__main__":
    myrequest = RailsbankRequest()
    # These are for getting the balance.
    #myrequest.makeEnduser()
    #myrequest.makeLedger()
    myrequest.fetchLedger()
    myrequest.showLedger()
    #myrequest.addMoney() #not needed
    print("\nWE ARE NOW GETTING BALANCE\n")
    myrequest.getBalance()
    #print("\nWE ARE NOW DOING PAYMENT\n")
    # These are for making a payment

    #requirements:

    print("\nMaking Beneficiaries\n")
    myrequest.makeBeneficiary()
    print("\nFetching Beneficiaries\n")
    myrequest.fetchBeneficiary()
    #myrequest.makePayment()
    # make payment
    # add benificary
    # request card
    # notify when money enters account
    #get req_card
    print("\nRequesting Card\n")
    myrequest.requestcard()
    #print("\nFetching Card\n")
    #myrequest.fetchCard()
    #print("\nActivating Card\n")
    #myrequest.activateCard()
