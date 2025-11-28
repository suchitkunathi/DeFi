import hashlib
import ecdsa
import binascii

class Wallet:
    def __init__(self):
        # Generate a new private key using SECP256k1 (Bitcoin curve)
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
        # Simple address generation: SHA256 of public key
        pub_key_bytes = self.public_key.to_string()
        sha256_bpk = hashlib.sha256(pub_key_bytes).hexdigest()
        return sha256_bpk

    def sign(self, message):
        # Sign a message (bytes)
        if isinstance(message, str):
            message = message.encode()
        signature = self.private_key.sign(message)
        return binascii.hexlify(signature).decode()

    @staticmethod
    def verify(message, signature_hex, public_key_hex):
        # Verify a signature
        if isinstance(message, str):
            message = message.encode()
        
        try:
            signature = binascii.unhexlify(signature_hex)
            # Reconstruct public key from hex (this part might need adjustment depending on how we store pubkeys)
            # For simplicity in this simulation, we might pass the VerifyingKey object or raw bytes.
            # Let's assume public_key_hex is the raw bytes hex.
            pub_key_bytes = binascii.unhexlify(public_key_hex)
            vk = ecdsa.VerifyingKey.from_string(pub_key_bytes, curve=ecdsa.SECP256k1)
            return vk.verify(signature, message)
        except (ecdsa.BadSignatureError, ValueError):
            return False

    def get_public_key_hex(self):
        return binascii.hexlify(self.public_key.to_string()).decode()
