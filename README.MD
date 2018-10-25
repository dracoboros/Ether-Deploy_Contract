# Contract Deployment in Web3.py

## Deploying contract in Rinkeby Test Network through Infura API

### Requirements:

- web3.py 4.7.2
- API Key from [infura.io](https://infura.io)
- Source account and its private key

```
infuraApi = 'API'
account = 'SRC ACCOUNT'
key = 'PRIVATE KEY'
```

#### Contract:

```
pragma solidity ^0.4.22;

contract HelloWorld {
    string public message;

    constructor() public {
        message = "Hello, World!";

    }

    function setMessage(string text) public payable{
        require(msg.value >= 0.01 ether);
        message = text;
    }

}
```

A simple "Hello, World" program that allows to change its message which call be called with <code>".message().call()"</code>.

#### Compiling the Contract:

```python
from utils import contractSource
from solc import compile_source

contractCompiled = compile_source(contractSource("HelloWorld"))
contractInterface = contractCompiled['<stdin>:HelloWorld']
```

###### Note: <code>contractSource</code> is a function defined in src/utils.py and its read the HelloWorld.sol file's content.

#### Creating the Contract:

```python
helloWorld = w3.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
```

<code>contractInterface</code> returns a <code>dict</code> with the Contracts inside of .sol file. In this cenario there is only one "HelloWorld".

#### Building the transaction and sending it:

##### Defining the transaction's parameters:

```python
txParams = {
    'gas': 2000000,
    'gasPrice': w3.eth.gasPrice,
    'nonce': w3.eth.getTransactionCount(account),
    'chainId': 4,  # Rinkeby Test Network
    'from': account
}
```

##### Associating transaction's parameters with the Contract:

```python
tx = helloWorld.constructor().buildTransaction(txParams)
```

##### Signing the transaction with creator account's private key:

```python
signedTx = w3.eth.account.signTransaction(tx, key)
```

##### Sending the transaction to the Rinkeby Test Network:

```python
txReceipt = w3.eth.sendRawTransaction(signedTx.rawTransaction)
```

If <code>sendRawTransaction</code> is successful it returns a hash: <code>0xea1bb31684fa63f13008f11c3ddbfed444835e9e8d0a279ff806e52b8e527b95</code>

which can be used to get the transaction's detail. Check in [rinkeby.etherscan.io](https://rinkeby.etherscan.io/tx/0xea1bb31684fa63f13008f11c3ddbfed444835e9e8d0a279ff806e52b8e527b95).

##### Getting transaction's detail:

```python
receipt = w3.eth.waitForTransactionReceipt(txReceipt)
```

The function above returns the following dictionary:

```python
AttributeDict({'blockHash': HexBytes('0x68dc9bc28a5e8fa2f5ff6325f13e8bd2f0560ca543bf011d71f9e1ed00f86e5c'),
 'blockNumber': 3224432,
 'contractAddress': '0x327fE98DaF48836e982396cF3cf4Bf468Ca11Ea8',
 'cumulativeGasUsed': 5460633,
 'from': '0xf31a44312c4cc8cfd207e5baa654f5597e461552',
 'gasUsed': 282543,
 'logs': [],
 'logsBloom': HexBytes('a lot of zeros'),
 'status': 1,
 'to': None,
 'transactionHash': HexBytes('0xea1bb31684fa63f13008f11c3ddbfed444835e9e8d0a279ff806e52b8e527b95'),
 'transactionIndex': 9})
```

The 'contractAddress' field will be used to interact with the deployed contract in the next section.

#### Defining the interface and interacting with it:

```python
helloWorldInstance = w3.eth.contract(
   receipt.contractAddress,
   abi=contractInterface['abi'],
)
```

```python
helloWorldInstance.functions.message().call() # returns "Hello, World!"
```
