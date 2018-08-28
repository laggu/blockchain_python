from block import Block
from transaction import Transaction
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import bitcoin


class BlockChain:
    def __init__(self):
        self.chain = []
        self.tx_pool = []
        self.bits = 2
        self.reward = 50

        genesis_block = Block(None, self.bits, [])
        genesis_block.bits = self.bits
        genesis_block.gen_hash()
        self.chain.append(genesis_block)

    def make_transaction(self, value, receiver_address, sender_address, sender_private_key):
        try:
            transaction = Transaction(self, value, receiver_address, sender_address, sender_private_key)
        except Exception as e:
            return str(e)
        self.tx_pool.append(transaction)
        return transaction.hash

    def mining(self, miner_address):
        tx_list = self.tx_pool
        tx_list.insert(0, Transaction(self, self.reward, miner_address))
        self.tx_pool = []
        new_block = Block(self.chain[-1].hash, self.bits, tx_list)
        try:
            new_block.gen_hash()
        except:
            return '블록 생성 실패'
        self.chain.append(new_block)
        return new_block.hash

    def get_utxo_list(self, address):
        utxo_list = []
        for block in self.chain:
            for tx in block.transactions:
                for i in range(len(tx.inputs)):
                    for utxo in utxo_list:
                        if tx.inputs[i].hash == utxo[0] and tx.inputs[i].n == utxo[1] and tx.inputs[i].address == utxo[2] and tx.inputs[i].value == utxo[3]:
                            utxo_list.remove((tx.inputs[i].hash, tx.inputs[i].n, tx.inputs[i].address, tx.inputs[i].value))
                for i in range(len(tx.outputs)):
                    if address == tx.outputs[i].to:
                        utxo_list.append((tx.hash, i, tx.outputs[i].to, tx.outputs[i].value))

        return utxo_list

    def get_balance(self, address):
        utxo_list = self.get_utxo_list(address)
        balance = 0
        for utxo in utxo_list:
            balance += utxo[3]

        return balance

    def increase_bits(self):
        self.bits += 1

    def decrease_bits(self):
        self.bits -= 1