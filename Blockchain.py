from Block import Block
from Persona import Persona
from Contract import Contract
import pickle
from os import chmod,path
from static import *
import json

class Blockchain:
    def __init__(self, party_balances_storage='storage/party_balances.pickle',previous_signature_storage='storage/previous_signature.pickle',blockchain_storage='storage/blockchain_record.pickle',address_keys_storage='storage/address_keys.pickle',nft_storage='storage/nfts.pickle'):
        
        self.persona = Persona()
        self.blockchain = []
        self.block_number = 0
        self.previous_signature = 'Genesis Signature Seed'
        self.address_keys = {AUTHORITY_ADDRESS:AUTHORITY_KEY_STR}
        #self.key_addresses = {AUTHORITY_KEY_STR:AUTHORITY_ADDRESS}
        self.nfts = {}
        self.party_balances = {AUTHORITY_ADDRESS:GENESIS_TOKENS}
        self.party_balances_storage = party_balances_storage
        self.previous_signature_storage = previous_signature_storage
        self.address_keys_storage = address_keys_storage
        self.blockchain_storage = blockchain_storage
        self.nft_storage = nft_storage
        self.latest_block_ts = get_ts()
        
        if path.exists(party_balances_storage):
            self.party_balances = pickle.load(open(party_balances_storage,'rb'))

        if path.exists(previous_signature_storage):
             self.previous_signature = pickle.load(open(previous_signature_storage,'rb'))

        if path.exists(address_keys_storage):
            self.address_keys = pickle.load(open(address_keys_storage,'rb'))

        if path.exists(nft_storage):
            self.nfts = pickle.load(open(nft_storage,'rb'))

        if path.exists(blockchain_storage):
            self.blockchain = pickle.load(open(blockchain_storage,'rb'))
            self.block_number = len(self.blockchain)
        else:
            c = Contract(AUTHORITY_ADDRESS.lower(),GENESIS_TOKENS,"Genesis Block",fee=0)
            self.add(c.get_signed_json())

            c2 = Contract('0DD7F8D140EBD5D3B2C9BC7E836D8E65393C6D808155066A9CF78AA2A029D97E'.lower(),9999999,"Transfer Tokens",data="",fee=0)
            self.add(c2.get_signed_json())
            """
            c2 = Contract(AUTHORITY_ADDRESS,0,"Mint NFT",data="NFT is being minted as the hash of this contract",fee=0)
            self.add(c2.get_signed_json())
            c3 = Contract('1fd7cdc50046c21ea50a87e7be589095ba28f31584d87f0a2f52d0b233945374',0,"Transfer NFT",data=c2.address,fee=0)
            self.add(c3.get_signed_json())
            c4 = Contract('1fd7cdc50046c21ea50a87e7be589095ba28f31584d87f0a2f52d0b233945374',10000,"Transfer Tokens",data=c2.address,fee=0)
            self.add(c4.get_signed_json())
            """

    def faucet(self,payload):
        #print(faucet_request_json)
        if self.block_number > FAUCET_LIMIT:
            return False
        #payload = json.loads(faucet_request_json)
        #print(payload)
        authority_address = payload['authority']
        #print(authority_address)
        if AUTHORITY_ADDRESS != authority_address:
            return False

        server = payload['server']
        if HOST != server:
            return False
        #party_key_str = rebend(payload['Public Key'])

        #party_address =  self.persona.get_key_address(party_key_str)       
        if payload['destination'] in self.party_balances:
            print("account exists")
            return False

        c = Contract(payload['destination'],FAUCET_TOKENS,"Faucet Transfer",fee=0)
        return self.add(c.get_signed_json())

            
    def store(self):
        with open(self.blockchain_storage,'wb') as bf:
            #pickle.dump(self.blockchain,bf)
            pickle.dump([str(o) for o in self.blockchain],bf)

        with open(self.previous_signature_storage,'wb') as bf:
            pickle.dump(self.previous_signature,bf)

        with open(self.party_balances_storage,'wb') as bf:
            pickle.dump(self.party_balances,bf)

        with open(self.nft_storage,'wb') as bf:
            pickle.dump(self.nfts,bf)

        with open(self.address_keys_storage,'wb') as bf:
            pickle.dump(self.address_keys,bf)

        self.latest_block_ts = get_ts()

    def get_address_key(self,address):
        address = address.lower()
        return self.address_keys[address]

    def get_address_balance(self,address):
        address = address.lower()
        tokens = 0 if address not in self.party_balances else self.party_balances[address]
        nft_count = 0 if address not in self.nfts else len(self.nfts[address])
        nft_list = '[]' if nft_count == 0 else str(list(self.nfts[address])).replace("'",'"')
        return '{"tokens":' + str(tokens) + ',"nft_count":' + str(nft_count) + ',"nft_list":' + nft_list + '}'

    def add(self,contract_json):
        contract = json.loads(contract_json)
        payload = contract['payload']
        authority_address = payload['authority'].lower()
        server = payload['server'].lower()

        if AUTHORITY_ADDRESS != authority_address:
            return False
        if HOST != server:
            return False
        party_key_str = rebend(contract['key'])
        origin = payload['origin'].lower()

        if origin not in self.address_keys:
            party_address = self.persona.get_key_address(party_key_str)
            if party_address != origin:
                print("origin does not match public key hash")
                return False
            self.address_keys[origin] = party_key_str

        if self.address_keys[origin] != party_key_str:
            print("origin does not match public key")
            return False

        destination = payload['destination'].lower()

        #print("get block number")
        self.block_number = len(self.blockchain)

        """
        print(self.party_balances[origin])
        print(origin)
        print(AUTHORITY_ADDRESS)
        """
        party_nfts = set() if origin not in self.nfts else self.nfts[origin]
        block = Block(contract_json,self.previous_signature,self.party_balances[origin],party_nfts,self.block_number,self.latest_block_ts)
        #print("return block")
        is_valid = block.validation_result

        if is_valid:
            self.previous_signature = block.authority_signature
            self.blockchain.append(block)
            self.party_balances[origin] -= (block.tokens + block.fee)
            if destination not in self.party_balances:
                self.party_balances[destination] = 0
            self.party_balances[destination] += block.tokens
            self.party_balances[AUTHORITY_ADDRESS] += block.fee
            if contract['payload']['type'] == "Mint NFT":
                if destination in self.nfts:
                    self.nfts[destination].add(contract['address'])
                else:    
                    self.nfts[destination] = set([contract['address']])
            if contract['payload']['type'] == "Transfer NFT":
                self.nfts[origin].remove(payload['data'])
                if destination not in self.nfts:
                    self.nfts[destination] = set()
                self.nfts[destination].add(payload['data'])
                
            self.store()
            return True
        return False

    def __str__(self):
        #return '\n\n'.join(["\nBlock Number: " + str(i) + '\n' + str(b) for i,b in enumerate(self.blockchain)])
        return '[' + ','.join([str(b) for b in self.blockchain]) + ']'

if __name__ == '__main__':
    k = Blockchain()
    print(k)
