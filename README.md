# Grantkey

## Introduction
[Grantkey](https://grantkey.com) is a lightning-fast blockchain that allows you to transfer tokens, mint NFTs, and write smart contracts with real-time clearing at negligible cost. You can connect as a user with nothing more than a modern browser. 

## Quick Start

### User Setup
To connect as a user, simply use any modern browser to open [grantkey.com](https://grantkey.com). When you load the page, a key pair will automatically be generated using javascript on the client-side meaning that only you will have access to your private key. Download your wallet and store it in a secure location. If you'd like to run your own blockchain as an Authority node, follow the instructions below in the "Server Setup" section.

### Authority Setup

#### Requirements
To run your own Authority node and separate blockchain, you will need your own https enabled domain name and server with nginx, Python 3.8, and pip installed. Use nginx to route traffic from port 443 to your instance.

#### Installation
To create your own blockchain, simply use the following commands.
```bash
    $ git clone git@github.com:Grantkey/prototype.git
    $ cd prototype/
    $ python3.8 -m venv env
    $ . env/bin/activate
    $ pip install -r requirements.txt 
    $ chmod +x start.sh
    $ ./start.sh
```
## Capabilities

### View History
Anyone can view and download the entire history of the blockchain [here](https://grantkey/fullchain/).

### Explore Blocks
Blocks can be explored via the block explorer API. Simply select the block number to view and enter it as follows: [https://grandkey.com/block/0](https://grandkey.com/block/0)

### Transfer Tokens
Transfer tokens simply by selecting the address to transfer them. As long as you have enough tokens to cover the exchange plus the blockchain fee, your transaction will compelete. 

### Destory Tokens (Coming Soon)
If you want to move your tokens to another blockchain, you might need to destroy them on the current blockchain, so this is an option.

### Mint NFT
To mint an NFT simply place the sha256 hash of the digital artifact you want to mint into the external data field. You can get the sha256 hash of any file using the command below:

```bash
    $ sha256sum filename.ext
```
### Transfer NFT
Transfer an NFT simply by selecting the destination address. As long as you have the NFT along with the tokens required to cover the blockchain fee, your transaction will compelete. 

### Destroy NFT (Coming Soon)
If you want to move your NFT to another blockchain, you might need to destroy it on the current blockchain, so this is an option.

### Send Data
Simply set the destination as the indended recipient of the data. Whatever is published to the blockchain will be visible to everyone.

### Oracle (Coming Soon)
Publish data that can be used for the settlement of contracts.

## Mechanics

### Overview
Grantkey achieves instantaneous contract clearing while maintaining a cryptographically secured, tamper resistant blockchain by moving from decentralized processing  / validation to authority-based processing with decentralized validation. The authority is prevented from cheating because it signs every block meaning that if it ever attempts to tamper with the blockchain, anyone with a receipt of a block signed by the authority that is not present in the blockchain will be able to prove that the authority tampered with the chain and a new authority will be selected.

### Process
By design, each transaction is processed as a new block serially in the order it is received. When a user decides to submit a transaction, a contract is generated and digitally signed by the user's private key. After that, it is submitted to the authority. Once the authority validates the contract, it signs the contract and publishes it to the blockchain. In this way, it can be proven that both the sender and the authority approved the contract. 

### [Contract](https://github.com/Grantkey/prototype/blob/master/Contract.py)
Each blockchain interaction is built on a contract which is signed by the user to prove its authenticity. The contract contains the details of the interaction as well as metadata about the authority and server in order to prevent spoofing across different blockchain instances.

### [Block](https://github.com/Grantkey/prototype/blob/master/Block.py)
Each block contains a signle signed contract that has been validated by the authority. To secure the blockchain, the authority combines the previous block signature with the current block data and digitally signs signs the blockto create a tamper resistant blockchain.

### [Blockchain](https://github.com/Grantkey/prototype/blob/master/Blockchain.py)
Since the signature of each block is based on the signature of the previous block, it is infeasible to alter the blockchain without detection. If the authority attempts to alter or remove a block, anyone with a valid authority signature that doesn't exist in the blockchain will be able to prove malfeasance on the part of the authority and a new authority can be selected. 

### [Authority](https://github.com/Grantkey/prototype/blob/master/Authority.py) 
The authority node allows users to connect and interact with the blockchain.
