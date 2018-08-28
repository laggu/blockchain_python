import time
import hashlib
import json
import copy

class Block:
    def __init__(self, prev_hash, bits, transactions):
        self.prev_hash = prev_hash
        self.timestamp = time.time()
        self.mrkl_root = None
        self.bits = bits
        self.nounce = 0
        self.hash = None
        self.transactions = transactions

    def gen_mrkl_root(self):
        if len(self.transactions) == 0:
             return None
        temp = [hashlib.sha256(str(x).encode()).hexdigest() for x in self.transactions]

        while not len(temp) == 1:
            if len(temp) % 2 == 1:
                temp.append(copy.copy(temp[-1]))
            temp = [hashlib.sha256((str(temp[i])+str(temp[i+1])).encode()).hexdigest() for i in range(0, len(temp), 2)]

        self.mrkl_root = temp[0]

    def gen_hash(self):
        # 이중 지불 검사 및 서명 검증
        for tx in self.transactions:
            try :
                tx.can_spent()
            except:
                raise Exception('트랜잭션 검증 실패')

        txin_list = []
        double_used_tx_list = []
        for tx in self.transactions:
            for txin in tx.inputs:
                if txin not in txin_list:
                    txin_list.append(txin)
                else:
                    double_used_tx_list.append(tx)
                    break

        print("self.transaction",self.transactions)
        print("double_used_tx_list",double_used_tx_list)

        for tx in double_used_tx_list:
            self.transactions.remove(tx)
        print("self.transaction", self.transactions)


        self.gen_mrkl_root()
        while True:
            h = hashlib.sha256(str(self).encode()).hexdigest()
            if h[:self.bits] == '0'*self.bits:
                self.hash = h
                break
            self.nounce += 1

    def __str__(self):
        return json.dumps(self, default=self.to_dict, sort_keys=True, indent=4)

    def to_dict(self, _):
        if '__dict__' not in dir(_):
            return str(_)
        temp = copy.deepcopy(_.__dict__)
        if "hash" in temp:
            del temp['hash']
        return temp

    def mystr(self):
        return json.dumps(self, default=self.to_mydict, sort_keys=True, indent=4)

    def to_mydict(self,_):
        if '__dict__' not in dir(_):
            return str(_)
        return copy.deepcopy(_.__dict__)
