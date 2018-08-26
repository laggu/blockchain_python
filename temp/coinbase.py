import hashlib
import json
from transaction import TxOut
import time
import copy


class Coinbase():
    def __init__(self, reward, miner_address):
        self.vin_sz = 0
        self.vout_sz = 0
        self.inputs = []
        self.outputs = []
        self.hash = None
        self.timestamp = time.time()

        txout = TxOut(miner_address, reward)
        self.outputs.append(txout)
        self.vout_sz = 1
        self.gen_hash()

    def gen_hash(self):
        self.hash = hashlib.sha256(str(self).encode()).hexdigest()

    def __str__(self):
        return json.dumps(self, default=self.to_dict, sort_keys=True, indent=4)

    def to_dict(self,_):
        temp = copy.deepcopy(_.__dict__)
        if "hash" in temp:
            del temp['hash']
        return temp

if __name__ == "__main__":
    coinbase = Coinbase(50, "1HUBHMij46Hae75JPdWjeZ5Q7KaL7EFRSD")
    print(coinbase)