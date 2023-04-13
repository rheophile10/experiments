from dotenv import dotenv_values
from cat_convos import CatConvo
from pathlib import Path


env_path = Path(__file__).parent / '.env'
config = dotenv_values(env_path)
BSKY_USERNAME = config["BSKY_USERNAME"]
BSKY_PASSWORD = config["BSKY_PASSWORD"]
ASSETS_PATH = Path(__file__).parent / 'assets'

c = CatConvo(BSKY_USERNAME, BSKY_PASSWORD, ASSETS_PATH)
x = c.rsa_message('hey how goes it')
c.stego_hide(x,ASSETS_PATH / 'message.png')
y=c.stego_reveal(ASSETS_PATH / 'message_steg.png')
with open(ASSETS_PATH / 'public.txt', 'r') as file:
    p = file.read()
print(c._decode_rsa(y, p))
