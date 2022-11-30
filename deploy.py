from solcx import compile_standard, install_solc
import json

from web3 import Web3
with open("SimpleStorage.sol","r") as file:
    simple_storage_file = file.read()
  #  print(simple_storage_file)


install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                }
            }
        },
    },
    solc_version="0.8.0",
)
#print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# bytecode getting

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

print(abi)

my_address = "0x567Da5ECad3Bb2a56E5954A07f92b7D01156fCF0"
private_key = "0x078e5e9f3277ee281089800d659faecb2a9ff9000d530395636045691454d2f8"
http_url="HTTP://172.25.112.1:7545"
chain_id = 1337
w3=Web3(Web3.HTTPProvider("HTTP://172.25.112.1:7545"))
print(w3)
#deployment

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)

#get the  latest transaction

nonce = w3.eth.getTransactionCount("0x567Da5ECad3Bb2a56E5954A07f92b7D01156fCF0")
print(nonce)

transaction = SimpleStorage.constructor().buildTransaction({"gasPrice":w3.eth.gas_price,"chainId":chain_id, "from":"0x567Da5ECad3Bb2a56E5954A07f92b7D01156fCF0", "nonce" : nonce})
print(transaction)

# sign the  transaction using private key

signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)

#send this  signed transaction

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

#receipt

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#working with the contract
#needed contract address & COntract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(simple_storage)