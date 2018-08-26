from transaction import TxOut
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


class UTXO:
    def __init__(self, transaction_hash, n, txout):
        self.transaction_hash = transaction_hash
        self.n = n
        self.txout = txout


class Wallet:
    def __init__(self, name):
        self.owner = name
        self.utxo_list = []
        self.total_value = 0

        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()
        digest = SHA256.new()
        digest.update(self.public_key)
        self.wallet_address = digest

    def add_utxo(self, transaction_hash, n, txout):
        utxo = UTXO(transaction_hash, n, txout)
        self.utxo_list.append(utxo)
        self.total_value += utxo.txout.value

    def get_utxo(self, value):
        temp = []
        if self.total_value < value:
            return temp

        current_value = 0
        for utxo in self.utxo_list[::-1]:
            current_value += utxo.txout.value
            temp.append(utxo)
            self.utxo_list.remove(utxo)
            if current_value >= value:
                break

        self.total_value -= current_value
        return temp, current_value