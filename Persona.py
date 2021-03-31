#!/usr/bin/env python
from os import chmod,path
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

class Persona:
    def __init__(self,key_size=3072,private_key_path="config/private_key.pem",public_key_path="config/public_key.pem"):
        self.key_size = key_size
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

        # Load or create private key
        self.private_key = self.get_private_key()

        # Load or create public key
        self.public_key = self.get_public_key()

    def get_private_key(self):
        if path.exists(self.private_key_path):
            private_key = RSA.importKey(open(self.private_key_path,'r').read())
        else:
            private_key = RSA.generate(self.key_size)
            with open(self.private_key_path, 'wb') as f:
                chmod(self.private_key_path, 0o600)
                f.write(private_key.exportKey('PEM'))
        return private_key

    def get_public_key(self):
        if path.exists(self.public_key_path):
            public_key = RSA.importKey(open(self.public_key_path,'r').read())
        else:
            public_key = self.private_key.publickey()
            with open(self.public_key_path, 'wb') as f:
                chmod(self.public_key_path, 0o600)
                f.write(public_key.exportKey('PEM'))
        return public_key

    def get_key_from_file(self,key_path):
        return RSA.importKey(open(key_path,'r').read())

    def get_key_from_str(self,key_str):
        return RSA.importKey(key_str)

    def get_msg_hash(self,msg):
        return SHA256.new(str.encode(msg))

    def get_msg_signature(self,msg):
        msg_hash = self.get_msg_hash(msg)
        return PKCS115_SigScheme(self.private_key).sign(msg_hash)

    def get_msg_signature_str(self,msg):
        return binascii.hexlify(self.get_msg_signature(msg)).decode('ascii')

    def validate_signature(self,msg,signature,signing_public_key=None):
        signing_public_key = self.public_key if signing_public_key is None else signing_public_key
        if isinstance(signing_public_key,str):
            signing_public_key = self.get_key_from_str(signing_public_key)
        msg_hash = self.get_msg_hash(msg)
        try:
            PKCS115_SigScheme(signing_public_key).verify(msg_hash, signature)
            return True
        except:
            return False

    def get_key_str(self,key):
        return str(key.exportKey('PEM'),'utf8')

    def get_key_address(self,key_str):
        return self.get_msg_hash(key_str).hexdigest()
        #return hashlib.md5(key_str.encode('utf8')).hexdigest()

    def get_address(self):
        return self.get_key_address(str(p))

    def __str__(self):
        return str(self.public_key.exportKey('PEM'),'utf8')

if __name__ == '__main__':
    p = Persona()
    print(p.get_address())
