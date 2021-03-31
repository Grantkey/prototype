#!/usr/bin/env python3
from Persona import Persona 
from Contract import Contract 
from static import *
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-k','--keyfile',dest='keyfile')
parser.add_argument('-t','--tokens',dest='tokens')
parser.add_argument('-s','--script',dest='script')
parser.add_argument('-a','--action',dest='action')
args = parser.parse_args()

p = Persona()

if args.keyfile is None:
    counterparty_key_str = PARTY_KEY_STR
else:
    counterparty_key_str = p.get_key_str(p.get_key_from_file(args.keyfile))

if args.tokens is None:
    args.tokens = 0

if args.script is None:
    args.script = "True"

if args.action is None:
    args.action = 'add'

if args.action not in {'add','faucet'}:
    print("INVALID ACTION")
    exit(0)

url = ''.join([HOST,':',str(PORT),'/',args.action])

# Add Contract
if args.action == 'add':
    c = Contract(destination,args.tokens,args.script)
    payload = c.get_signed_json()

# Request Tokens From Faucet
if args.action == 'faucet':
    payload = '{"Authority":"' + AUTHORITY_ADDRESS + '","Destination":"' + PARTY_ADDRESS + '"}'

response = requests.post(url, json=payload)
print(response.text)
