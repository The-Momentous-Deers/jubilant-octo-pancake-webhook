import json, time, pprint
from urllib.request import Request, urlopen
import urllib.error

base_url = 'https://playlive.railsbank.com/'

# The next line contains get post and put helper functions, which should be replaced with a library of your choice in production code
custom_fetch = lambda method, relative_url, body=None: json.loads(urlopen(Request(base_url+relative_url, data=json.dumps(body).encode('utf8'), method=method, headers={'Content-Type': 'application/json', 'Authorization': 'API-Key ' + api_key, 'Accept': 'application/json'})).read().decode('utf-8')); post = lambda url, body=None: custom_fetch("POST", url, body); get = lambda url: custom_fetch("GET", url); put = lambda url, body=None: custom_fetch("PUT", url, body)

# Make sure to replace `***EXAMPLE KEY***` in the next line with your api key of form <key_id>#<key_secret>
api_key = 'ayzmam4ta3uu3n1quuvq8u0m3kcl4vnx#6sipzuhpoemrwr1kvcgxe0dtjnneryjg0lngqbq9l777j89jsv8th28pferkt43g'


class RailsbankRequest:

    def __init__(self):
        # This needs to fetch the relevant data from the database
        # data includes, ledgerID, benifactoryID, enduserID?
        response = get('v1/customer/me')
        # pprint.pprint(response)
        self.customer_id = response['customer_id']

    def makeBeneficiary(self):
        '''
        Creating beneficiary for our enduser.
        '''
        response = post(
            'v1/customer/beneficiaries', {
                'holder_id': self.enduser_id,
                'asset_class': 'currency',
                'asset_type': 'eur',
                #'iban': 'SK4402005678901234567890',
                #'bic_swift': 'SUBASKBX',
                'uk_account_number': '12345678',
                'uk_sort_code': '123434',
                'person': {
                    'name': 'Peter',
                    'address': {
                        'address_iso_country': 'GB',
                        'address_postal_code': "PO5 1OD",
                        'address_number': "420"
                    },
                    'email': 'peter@email.com'
                }
            })
        pprint.pprint(response)
        self.beneficiary_id = response['beneficiary_id']

        '''
        Beneficiary is not ready immediately because of ongoing validity checks.
        '''
        response = get('v1/customer/beneficiaries/' + str(self.beneficiary_id) + '/wait')


    def getEnduser(self):
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

        '''
        Enduser is not ready immediately because of ongoing validity checks.
        '''
        #response = get('v1/customer/endusers/' + str(self.enduser_id) + '/wait')
        #pprint.pprint(response)



    def makeLedger(self):
        '''
        Creating ledger assigned to our enduser and assigning iban to it.
        '''
        bank_example_product = 'PayrNet-GBP-1'
        response = post(
            'v1/customer/ledgers', {
                'holder_id': self.enduser_id, # this was self.enduser_id
                'partner_product': bank_example_product,
                'asset_class': 'currency',
                'asset_type': 'gbp',
                'ledger-type': 'ledger-type-single-user',
                'ledger-who-owns-assets': 'ledger-assets-owned-by-me',
                'ledger-primary-use-types': ['ledger-primary-use-types-payments'],
                'ledger-t-and-cs-country-of-jurisdiction': 'GB'
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


    def getBalance(self):
        response = get('v1/customer/ledgers/' + str(self.ledger_id))
        pprint.pprint(response["amount"])

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


    def requestcard(self):
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
        #pprint.pprint(self.enduser_id)
        #finshed creating a card holding end user
        #Issueing an enduser with a EUR ledger
        response = post(
        'v1/customer/ledgers',{
            "holder_id": self.enduser_id,
	        "partner_product": "PayrNet-GBP-1",
	        "asset_class": "currency",
	        "asset_type": "gbp",
            "ledger_type": "ledger-type-single-user",
            "ledger_who_owns_assets": "ledger-assets-owned-by-me",
            "ledger_primary_use_types": ["ledger-primary-use-types-payments"],
            "ledger_t_and_cs_country_of_jurisdiction": "GBR"
            })#returns ledger_id in a dictionary
        self.ledger_id = response['ledger_id']
        pprint.pprint("\nGonna print the first ledger ID\n")
        pprint.pprint(self.ledger_id)
        #Finished issueing an enduser with a EUR ledger
        #issueing the card
        pprint.pprint("self.ledger_id = ")
        pprint.pprint(self.ledger_id)
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

        #get('v1/customer/cards/'+self.card_id)


        pprint.pprint(response)



        #response = get https://live.railsbank.com/v1/customer/cards/{{card_id}}


if __name__ == "__main__":
    myrequest = RailsbankRequest()
    # These are for getting the balance.
    myrequest.getEnduser()
    #yrequest.makeLedger()
    #myrequest.addMoney() #not needed
    #myrequest.getBalance()
    print("\nWE ARE NOW DOING PAYMENT\n")
    # These are for making a payment
    #myrequest.makeBeneficiary()
    #myrequest.makePayment()
    # make payment
    # add benificary
    # request card
    # notify when money enters account
    #get req_card
    print("\nRequesting Card\n")
    myrequest.requestcard()
