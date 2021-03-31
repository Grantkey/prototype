from Persona import Persona
from static import *
import binascii as ba
import json

class Block:
    def __init__(self, contract_json, prior_signature,party_balance,party_nfts,block_number):
        self.persona = Persona()
        self.contract_json = contract_json
        #contract_str_tmp = contract_json.replace('{"Payload":','')
        #marker_start = ',"Payload":'
        #self.contract_str = contract_json[contract_json.find(',"Payload":') + len(marker_start):contract_json.find(',"Signature":"')]
        self.contract = json.loads(contract_json)
        self.payload = self.contract["payload"]
        self.payload_str = get_contract_json_str(self.payload) #TODO get this into static!
        #print(self.contract_str)
        self.contract_signature = ba.unhexlify(self.contract["signature"])
        self.tokens = int(self.payload["tokens"])
        self.fee = int(self.payload["fee"])
        self.party_key_str = rebend(self.contract["key"])
        #self.counterparty_key_str = rebend(self.payload["Counterparty Key"])
        self.prior_signature = prior_signature
        self.party_balance = party_balance
        self.party_nfts = party_nfts
        self.block_number = block_number
        self.validation_timestamp = get_ts()
        self.validation_result = self.validate_contract()
        self.evaluation_ready = self.evaluate_execution_time()
        self.evaluation_result = self.evaluate_contract()
        self.authority_signature = self.persona.get_msg_signature_str(str(prior_signature) + str(block_number) + self.contract_json) if self.validation_result else None
        self.block_fields = [
            "block",
            "contract",
            #"Authority",
            #"Contract Address",
            #"Contract Type",
            #"Origin",
            #"Destination",
            #"Terms",
            #"Data",
            #"Tokens",
            #"Effective Timestamp",
            #"Fee",
            #"Contract Key",
            #"Contract Signature",
            "timestamp",
            "evaluation",
            "signature",
        ]

        self.block_data = [
            self.block_number,
            self.contract_json,
            #self.payload["authority"],
            #self.contract["address"],
            #self.payload["type"],
            #self.payload["origin"],
            #self.payload["destination"],
            #self.payload["terms"],
            #self.payload["data"],
            #self.tokens,
            #self.payload["effective"],
            #self.fee,
            #self.contract["key"],
            #self.contract["signature"],
            self.validation_timestamp,
            self.evaluation_result,
            self.authority_signature,
        ]

    def validate_contract(self):
        # Validation code here
        #print("validate")
        if self.payload["tokens"] != str(self.tokens):
            print("invalid token value")
            return False
        #print("validate1")
        if self.fee < 1 and self.payload["origin"] != AUTHORITY_ADDRESS:
            print("invalid fee value")
            return False
        #print("validate2")
        if self.tokens < 0:
            print("invalid token value")
            return False
        #print("validate3")
        if (self.tokens + self.fee) > self.party_balance:
            print("not enough tokens for contract")
            return False
        #print("validate4")
        if self.payload["type"] == "Transfer NFT":
            if self.payload["data"] not in self.party_nfts:
                print("NFT does not belong to party")
                return False

        #print("validate5")
        return self.persona.validate_signature(self.payload_str,self.contract_signature,self.party_key_str)

    def evaluate_execution_time(self):
        # Evaluation code here
        return True

    def evaluate_contract(self):
        # Evaluation code here
        if not self.evaluation_ready:
            return False
        return True

    def __str__(self):
        if self.validation_result:
            #return "\n\n  "  + '\n\n  '.join([self.block_fields[i] + ":  " + str(e) for i,e in enumerate(self.block_data)]) + "\n\n  --------------\n"
            #return '{"'  + '","'.join([self.block_fields[i] + '":"' + unbend(e) for i,e in enumerate(self.block_data)]) + '"}'
            return '{"block":"' + str(self.block_number) + '","contract":'+ self.contract_json + ',"timestamp":"' + str(self.validation_timestamp) + '","evaluation":"' + str(self.evaluation_result) + '","signature":"' + self.authority_signature + '"}'
        return "  INVALID CONTRACT"

if __name__ == '__main__':
    from Contract import Contract
    """
    c = Contract()
    b = Block(c.get_signed_json(),'fake_sig',10,{'aaa','bbb'},1)
    #print(c.get_signed_json())
    print(b)
    """
    d = Contract(contract_type="Transfer NFT",data="aaa")
    x = Block(d.get_signed_json(),'fake_sig',10,{'aaa','bbb'},1)
    print(x)

