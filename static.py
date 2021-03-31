from Persona import Persona
p = Persona()
from datetime import timezone,datetime

utc_ts = datetime.now().replace(tzinfo = timezone.utc).timestamp
get_ts = lambda: str(datetime.now(timezone.utc))

MB = 10485760
HOST = "http://localhost"
PORT = 59999
AUTHORITY_KEY = p.get_key_from_file("config/authority.key")
AUTHORITY_KEY_STR = p.get_key_str(AUTHORITY_KEY)
AUTHORITY_ADDRESS = p.get_key_address(AUTHORITY_KEY_STR)
PARTY_KEY = p.public_key
PARTY_KEY_STR = str(p)
PARTY_ADDRESS = p.get_key_address(PARTY_KEY_STR)
GENESIS_TOKENS = 100000000
FAUCET_LIMIT = 500
FAUCET_TOKENS = 100

CONTRACT_FIELDS = [
            'authority',
            'created',
            'type',
            'origin',
            'destination',
            #'terms',
            'data',
            'tokens',
            'effective',
            'fee',
        ]

def unbend(s):
    return str(s).replace('\n','\\n')

def rebend(s):
    return str(s).replace('\\n','\n')

def get_contract_field_str_data(payload):
        return ''.join([unbend(payload[e]) for e in CONTRACT_FIELDS])

def get_contract_json_str(payload):
        return '{"' + '","'.join([e + '":"' + unbend(payload[e]) for e in CONTRACT_FIELDS]) + '"}'

def extract_signed_json(d):
        return '{"address":"' + d['address'] + '","payload":' + get_contract_json_str(d['payload']) + ',"key":"' + unbend(d['key']) + '","signature":"' + d['signature'] + '"}'
