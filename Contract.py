#!/usr/bin/env python
import uuid
from Persona import Persona
import binascii as ba
from static import *

class Contract:
    """
    Attributes:
        id (string) <- uuid identifier for contract (prevents replay)
        creation_timestamp (string)  <- ISO timestamp of contract creation (must be same day)
        authority_key_str (string) <- public key of authority
        party_key_str (string) <- public key of contract initiator
        counterparty_key_str (string) <- public key of contract counterparty              
        terms (string) <- GKScript for boolean evaluation; if true, transfer tokens to counterparty
        tokens (integer) <- tokens to transfer to counterparty if contract conditions are met
        execution_time (string) <- ISO timestamp at which the contract should be executed
        fee (integer) <- tokens to transfer back to network in exchange for contract processing
    """
    def __init__(self,counterparty_address=PARTY_ADDRESS, tokens=0, contract_type="Token Transfer", data="", execution_time=None,fee=1):

        p = Persona()
        self.id = str(uuid.uuid4())
        self.creation_timestamp = get_ts() #utc_ts()
        self.authority_address = AUTHORITY_ADDRESS
        self.server = HOST
        self.party_key_str = PARTY_KEY_STR
        self.party_address = p.get_key_address(PARTY_KEY_STR)
        self.counterparty_address = counterparty_address
        self.type = contract_type
        self.data = data
        self.tokens = tokens
        self.execution_time = execution_time
        self.fee = fee
        if execution_time is None:
            self.execution_time = get_ts() #utc_ts()

        self.payload_fields = [
            'authority',
            'server',
            'created',
            'type',
            'origin',
            'destination',
            'data',
            'tokens',
            'effective',
            'fee',
        ]

        self.payload_data = [
            #self.party_key_str,
            self.authority_address,
            self.server,
            self.creation_timestamp, 
            self.type,           
            self.party_address,
            self.counterparty_address,
            #self.terms,
            self.data,
            self.tokens,
            self.execution_time,
            self.fee,
        ]

        #self.unsigned_contract = self.get_contract_json()
        self.contract_json = self.get_contract_json()
        self.signature = p.get_msg_signature(self.get_contract_json())
        self.address = p.get_msg_hash(self.get_contract_json()).hexdigest()

    def get_contract_json(self):
        return '{"' + '","'.join([self.payload_fields[i] + '":"' + unbend(e) for i,e in enumerate(self.payload_data)]) + '"}'

    def get_contract_field_data(self):
        return ''.join([unbend(e) for i,e in enumerate(self.payload_data)])

    def get_signed_json(self):
        return '{"address":"' + self.address + '","payload":' + self.get_contract_json() + ',"key":"' + unbend(self.party_key_str) + '","signature":"' + self.get_signature_str() + '"}'

    def get_signature_str(self):
        return ba.hexlify(self.signature).decode('ascii')

    def get_contract_str(self):
        return ('\n\n'.join([self.payload_fields[i] + ":\n" + str(e) for i,e in enumerate(self.payload_data)]) + "\n\nsignature:\n" + self.get_signature_str())

    def __str__(self):
        return self.get_signed_json()        
        #return self.get_contract_str()        

if __name__ == '__main__':
    c = Contract()
    print(c)
