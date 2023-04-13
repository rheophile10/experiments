
#from atprototools import Session
from pathlib import Path
from typing import Optional, Tuple

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from stegano import lsb
from PIL import Image

class CatConvo:
    def __init__(self, username:str, password:str, assets_dir:Path, public_key_image:Optional[Path] =None, 
                 private_key_path: Optional[Path]=None, public_key_path: Optional[Path] = None)->None:
        
        self.username = username
        self.password = password

        public_key_image = assets_dir / 'public.png' if not public_key_image else public_key_image
        private_key_path = assets_dir / 'private.txt' if not private_key_path else private_key_path
        public_key_path = assets_dir / 'public.txt' if not public_key_path else public_key_path

        if private_key_path.exists():
            with open(private_key_path, 'rb') as file:
                self.private_key = file.read()

        if public_key_path.exists():
            with open(public_key_path, 'rb') as key_file:
                self.public_key_image = self.stego_hide(key_file.read().decode('utf-8'), public_key_image)
        else:
            self.private_key, public_key_str = self._keygen()
            self._save_key(self.private_key, private_key_path)
            self._save_key(public_key_str, public_key_path)
            self.public_key_image = self.stego_hide(public_key_str.decode('utf-8'), public_key_image)
        
    def _save_key(self, key:str, path:Path)->None:
        with open(path, 'wb') as file:
            file.write(key)

    def _keygen(self)->Tuple[bytes, bytes]:
        """Generate a public and private key pair using RSA encryption"""
        
        # Generate the RSA key pair
        key = RSA.generate(2048)
        
        # Get the private key in PEM format
        private_key = key.export_key()
        
        # Get the public key in PEM format
        public_key = key.publickey().export_key()
        
        # Return the keys as a tuple of strings
        return (public_key, private_key)

    def stego_hide(self, message: str, image: Path)->Path:
        steg_img_path = image.parent / (image.stem + '_steg' + image.suffix)
        steg_img = lsb.hide(image, message)
        steg_img.save(steg_img_path)
        return steg_img_path
    
    def stego_reveal(self, image:Path)->str:
        encrypted_str = lsb.reveal(image)
        return encrypted_str

    def rsa_message(self, message: str) -> str:
        """Embed a message in the LSB of an image file and return the path of the new image file"""
        

        key = RSA.import_key(self.private_key)
        

        cipher = PKCS1_OAEP.new(key)
        

        encrypted_data = cipher.encrypt(message.encode("UTF-8"))
        

        return encrypted_data.hex()
    
    def _decode_rsa(self, message: str, other_public_key: str) -> str:
        """Decode an image that has been encoded using the _encode_image function"""
        
        # Read the encoded message from the image file
        
        encrypted_data = bytes.fromhex(message)
        
        # Create an RSA key object from the other party's public key
        other_key = RSA.import_key(other_public_key)
        
        # Create an RSA cipher object using the other party's public key
        cipher = PKCS1_OAEP.new(other_key)
        
        # Decrypt the encoded message using the RSA cipher object
        decoded_data = cipher.decrypt(encrypted_data)
        
        # Return the decoded message as a string
        return decoded_data.decode("UTF-8")


