from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import bitcoin
import json
import time
import copy


class TxIn:
    def __init__(self, utxo):
        self.hash = utxo[0] # 사용할 UTXO가 포함된 트랜잭션 해쉬
        self.n = utxo[1] # 위 트랜잭션 중에서 몇번째 UTXO인지
        self.address = utxo[2] #위 UTXO의 수신주소 ( 그러니까 공개키 해쉬 )
        self.value = utxo[3] #위 UTXO의 잔액
        self.pubk = None #사용자의 공개키
        self.sign = None #서명

    def __str__(self):
        return json.dumps(self, default=self.to_dict, sort_keys=True, indent=4)

    def to_dict(self, _):
        temp = copy.deepcopy(_.__dict__)
        if "sign" in temp:
            del temp['sign']
        return temp

    def __eq__(self, other):
        return self.hash == other.hash and self.n == other.n

    def mystr(self):
        return json.dumps(self, default=self.to_mydict, sort_keys=True, indent=4)

    def to_mydict(self,_):
        if '__dict__' not in dir(_):
            return str(_)
        return copy.deepcopy(_.__dict__)

class TxOut:
    def __init__(self, receiver_address, value):
        self.to = receiver_address #받는놈 주소
        self.value = value #금액

    def __str__(self):
        return json.dumps(self, default=self.to_dict, sort_keys=True, indent=4)

    def to_dict(self,_):
        temp = copy.deepcopy(_.__dict__)
        if "hash" in temp:
            del temp['hash']
        return temp


class Transaction:
    def __init__(self, blockchain, value, receiver_address, sender_address=None, sender_private_key=None):
        self.vin_sz = 0
        self.vout_sz = 0
        self.inputs = []
        self.outputs = []
        self.hash = None
        self.timestamp = time.time()

        if sender_address is None:
            txout = TxOut(receiver_address, value)
            self.outputs.append(txout)
            self.vout_sz = 1
            self.gen_hash()
            return

        utxo_list = []
        for block in blockchain.chain:
            for tx in block.transactions:
                for i in range(len(tx.outputs)):
                    if sender_address == tx.outputs[i].to:
                        utxo_list.append((tx.hash, i, tx.outputs[i].to, tx.outputs[i].value))
                for i in range(len(tx.inputs)):
                    for utxo in utxo_list:
                        if tx.inputs[i].hash == utxo[0] and tx.inputs[i].n == utxo[1] and tx.inputs[i].address == utxo[2] and tx.inputs[i].value == utxo[3]:
                            utxo_list.remove((tx.inputs[i].hash, tx.inputs[i].n, tx.inputs[i].address, tx.inputs[i].value))

        for tx in blockchain.tx_pool:
            for i in range(len(tx.inputs)):
                for utxo in utxo_list:
                    if tx.inputs[i].hash == utxo[0] and tx.inputs[i].n == utxo[1] and tx.inputs[i].address == utxo[2] and tx.inputs[i].value == utxo[3]:
                        utxo_list.remove((tx.inputs[i].hash, tx.inputs[i].n, tx.inputs[i].address, tx.inputs[i].value))

        total_utxo_value = 0
        i = 0
        for utxo in utxo_list:
            total_utxo_value += utxo[3]
            i += 1
            if total_utxo_value >= value:
                utxo_list = utxo_list[:i]
                break

        if total_utxo_value < value:
            raise Exception("잔액 부족")

        for utxo in utxo_list:
            input = TxIn(utxo)
            self.inputs.append(input)
        self.vin_sz = len(self.inputs)

        self.sign(sender_private_key)

        if total_utxo_value == value:
            output = TxOut(receiver_address, value)
            self.outputs.append(output)
        else:
            output = TxOut(receiver_address, value)
            self.outputs.append(output)
            output = TxOut(sender_address, total_utxo_value-value)
            self.outputs.append(output)

        self.gen_hash()

    def can_spent(self):
        for input in self.inputs:
            print(input)
            print(input.hash)
            if not bitcoin.ecdsa_verify(bitcoin.sha256(str(input)),input.sign,input.pubk):
                raise Exception()

    def gen_hash(self):
        self.vout_sz = len(self.outputs)
        # self.hash = SHA256.new(str(self).encode()).hexdigest()
        self.hash = bitcoin.sha256(str(self))

    def sign(self, priv):
        # tx_in들에 sign에 self.hash에 대한 서명을 작성
        for tx_in in self.inputs:
            # digest = SHA256.new(str(tx_in).encode())
            # signer = PKCS1_v1_5.new(priv)
            # tx_in.sign = signer.sign(digest)  # 서명
            # tx_in.pubk = str(priv.publickey())
            tx_in.pubk = bitcoin.privkey_to_pubkey(priv)
            digest = bitcoin.sha256(str(tx_in))
            tx_in.sign = bitcoin.ecdsa_sign(digest, priv)

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