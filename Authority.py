#!/usr/bin/env python
from flask import Flask,g,jsonify,render_template,request
from waitress import serve
from Block import Block
from Persona import Persona
from Contract import Contract
from Blockchain import Blockchain
import json
from static import *
import os
from flask import send_from_directory

blockchain = Blockchain()

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/',strict_slashes=False)
def index():
    return render_template('index.html') 

@app.route('/add',methods=['POST'],strict_slashes=False)
def add():
    is_valid = blockchain.add(extract_signed_json(request.json))
    msg = str(blockchain.blockchain[-1]) if is_valid else '{"status":"invalid"}'
    return msg

@app.route('/key/<string:address>',strict_slashes=False)
def key(address):
    return blockchain.get_address_key(address)

@app.route('/balance/<string:address>',strict_slashes=False)
def balance(address):
    return blockchain.get_address_balance(address)

@app.route('/block/<int:block_number>',strict_slashes=False)
def block(block_number):
    if block_number > len(blockchain.blockchain) - 1:
        return "Invalid Block"
    return str(blockchain.blockchain[block_number]).replace('\n','<br>')

@app.route('/view/<int:block_number>',strict_slashes=False)
def view(block_number):
    if block_number > len(blockchain.blockchain) - 1:
        return "Invalid Block"
    return str(blockchain.blockchain[block_number]).replace('\n','<br>')


@app.route('/recent',strict_slashes=False)
def recent():
    if len(blockchain.blockchain) > 10:
        return str(blockchain.blockchain[-10:][::-1]).replace("'","")
    return str(blockchain.blockchain).replace("'","")
        

@app.route('/faucet',methods=['POST'],strict_slashes=False)
def faucet():
    if (blockchain.faucet(request.json)):
        return "TOKENS GRANTED"
    return "REQUEST FAILED"

"""
@app.route('/echo',methods=['POST'],strict_slashes=False)
def echo():
    print("ECHO")
    print(request.json)
    return '{"status":"valid"}'
"""

if __name__ == "__main__":
    #serve(app, host='0.0.0.0', port=PORT, url_scheme='https')
    serve(app, host='0.0.0.0', port=PORT)
