from flask import Flask, render_template, request, jsonify
from blockchain import BlockChain
import bitcoin
import json

app = Flask(__name__)

blockChain = BlockChain()


@app.route('/')
def index():
    return render_template('index.html')


# 키 생성
@app.route('/generatekey')
def generatekey():
    keyword = request.args.get('keyword')
    mypriv = bitcoin.sha256(keyword)
    mypubl = bitcoin.privkey_to_pubkey(mypriv)
    myaddress = bitcoin.pubkey_to_address(mypubl)
    myInfo = {
        'mypriv': mypriv,
        'mypubl': mypubl,
        'myaddress': myaddress
    }
    return json.dumps(myInfo)


# 블록 마이닝
@app.route('/mining')
def mining():
    minerAddress = request.args.get('minerAddress')
    block_hash = blockChain.mining(minerAddress)
    # 해당 블록의 해쉬값 전달
    blockHash = {
        'blockhash': block_hash
    }

    return json.dumps(blockHash)


# transaction 생성
@app.route('/transaction')
def transaction():
    value = int(request.args.get('value'))
    senderAddress = request.args.get('senderAddress')
    receiverAddress = request.args.get('receiverAddress')
    senderPriv = request.args.get('senderPriv')

    tx_hash = blockChain.make_transaction(value, receiverAddress, senderAddress, senderPriv)
    txHash = {
        'txhash': tx_hash
    }
    return json.dumps(txHash)


# 잔액 조회
@app.route('/balance')
def balance():
    address = request.args.get('balance')
    balance = {
        'balance': blockChain.get_balance(address)
    }
    return json.dumps(balance)


# 블록 조회
@app.route('/checkBlock')
def checkBlock():
    blockHash = request.args.get('myblock_hash')
    blockJ = {}
    for block in blockChain.chain:
        if block.hash == blockHash:
            blockJ['block'] = block.mystr()
            return json.dumps(blockJ)
    blockJ['block'] = '블록 탐색 실패'
    return json.dumps(blockJ)


# 트랜잭션 조회
@app.route('/checkTransaction')
def checkTransaction():
    transactionHash = request.args.get('mytransaction_hash')
    transactionJ = {}
    for block in blockChain.chain:
        for tx in block.transactions:
            if tx.hash == transactionHash:
                transactionJ['transaction'] = tx.mystr()
                return json.dumps(transactionJ)
    transactionJ['transaction'] = '트랜잭션 탐색 실패'
    return json.dumps(transactionJ)


# 블록 전체 조회
@app.route('/checkAllBlock')
def checkAllBlock():
    blocks = {}
    for i in range(len(blockChain.chain)):
        blocks[i] = blockChain.chain[i].mystr()
    blocks['n'] = len(blockChain.chain)
    print(blocks)
    return json.dumps(blocks)


app.run(host='localhost', port=9000)