import hashlib
import ecdsa
import binascii

class Wallet:
    def __init__(self):
                                                                    
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
                                                         
        pub_key_bytes = self.public_key.to_string()
        sha256_bpk = hashlib.sha256(pub_key_bytes).hexdigest()
        return sha256_bpk

    def sign(self, message):
                                
        if isinstance(message, str):
            message = message.encode()
        signature = self.private_key.sign(message)
        return binascii.hexlify(signature).decode()

    @staticmethod
    def verify(message, signature_hex, public_key_hex):
                            
        if isinstance(message, str):
            message = message.encode()
        
        try:
            signature = binascii.unhexlify(signature_hex)
                                                                                                                 
                                                                                                    
                                                               
            pub_key_bytes = binascii.unhexlify(public_key_hex)
            vk = ecdsa.VerifyingKey.from_string(pub_key_bytes, curve=ecdsa.SECP256k1)
            return vk.verify(signature, message)
        except (ecdsa.BadSignatureError, ValueError):
            return False

    def get_public_key_hex(self):
        return binascii.hexlify(self.public_key.to_string()).decode()
