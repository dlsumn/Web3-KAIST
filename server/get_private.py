import json
from web3 import Web3
from web3.auto import w3

with open('../ethereum/data/keystore/UTC--2023-05-14T15-39-40.084268687Z--697ddd0ceaa10578323b577bb341c74ce3830253', 'r') as f:
    keystore = json.load(f)

password = ''

private_key = w3.eth.account.decrypt({"address":"697ddd0ceaa10578323b577bb341c74ce3830253","crypto":{"cipher":"aes-128-ctr","ciphertext":"46ec7b549feef67bcf966cef2b81936021aa5ce30527b8e1638717a984415fef","cipherparams":{"iv":"a2cd8f2aca1c174d9f64ee2e92ae7213"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"954b15b0290a1f4580231327865dca67d91def8e91911875d3d8f561cfa9cdcc"},"mac":"507bc3e2cfe9fff10110fb25589cdd8f0d25fd29b52ee01e814a18de6b2fd1ea"},"id":"c264af38-cd25-43b1-9a26-82ff7967660b","version":3}, password)

print(private_key)
