import datetime, hashlib, json


class Blockchain:
    def __init__(self, pow = 4) -> None:
        self.chain = []
        self.len = 0
        self.create_block(1, '0')
        self.pow = pow

    def create_block(self, proof, prev_hash):
        block = {"index": self.len+1,
                  "proof": proof,
                 "timestamp": str(datetime.datetime.now()),
                  "prev_hash": prev_hash,
                 }
        self.len+=1
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    # Create block here then return it
    def proof_of_work(self, prev_proof) -> str:
        new_proof = 1
        while True:
            hash_op = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            # print("Trying: ", hash_op)
            if hash_op[:self.pow] == "0"*self.pow:
                print(f"Found: {hash_op} with nonce: {new_proof}")
                return new_proof
            new_proof+=1
    
    def hash(Self, block) -> str:
        enc_block = json.dumps(block).encode()
        return hashlib.sha256(enc_block).hexdigest()

    def is_chain_valid(self) -> bool:
        prev_block = self.chain[0]
        for block in self.chain[1:]:
            if block["prev_hash"] != self.hash(prev_block):
                return False
            prev_proof = prev_block["proof"]
            curr_proof = block["proof"]
            hash_op = hashlib.sha256(str(curr_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_op[:4] != "0000":
                return False
            prev_block = block
            
        return True