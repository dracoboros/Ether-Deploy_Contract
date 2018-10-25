from utils import contractSource
from solc import compile_source
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

infuraApi = ''
account = ''
key = ''

w3 = Web3(HTTPProvider(f"https://rinkeby.infura.io/v3/{infuraApi}"))

contractCompiled = compile_source(contractSource("HelloWorld"))
contractInterface = contractCompiled['<stdin>:HelloWorld']
helloWorld = w3.eth.contract(
    abi=contractInterface['abi'], bytecode=contractInterface['bin'])
txParams = {
    'gas': 2000000,
    'gasPrice': w3.eth.gasPrice,
    'nonce': w3.eth.getTransactionCount(account),
    'chainId': 4,  # Rinkeby Test Network
    'from': account
}

tx = helloWorld.constructor().buildTransaction(txParams)
signedTx = w3.eth.account.signTransaction(tx, key)
txReceipt = w3.eth.sendRawTransaction(signedTx.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(txReceipt)

helloWorldInstance = w3.eth.contract(
    receipt.contractAddress,
    abi=contractInterface['abi'],
)

print(helloWorldInstance.functions.message().call())
