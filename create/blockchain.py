import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse


class Blockchain:
    def __init__(self, port) -> None:
        self.chain = []
        self.port = port
        self.nodes_discovery_lock = False
        self.len = 0
        self.transactions = []
        self.nodes = set()
        self.create_block(1, '0')
        self.pow = 4

    def mine_block(self, node_address, reciever):
        prev_block = self.get_prev_block()
        prev_proof = prev_block["proof"]
        proof = self.proof_of_work(prev_proof)
        prev_hash = self.hash(prev_block)
        self.add_transaction(node_address, reciever, 10)
        block = self.create_block(proof, prev_hash)
        return block

    def create_block(self, proof, prev_hash):
        block = {"index": self.len+1,
                 "proof": proof,
                 "timestamp": str(datetime.datetime.now()),
                 "prev_hash": prev_hash,
                 "transactions": self.transactions
                 }
        self.len += 1
        self.chain.append(block)
        self.transactions = []
        self.notify_nodes()

        return block

    def notify_nodes(self):
        print("notifing nodes")
        for node in self.nodes:
            response = requests.get(f"http://{node}/replace")
            if response.status_code == 200:
                result = response.json()
                message = result["message"]
                if message == "Different":
                    print(f"Replaced {node} with current value")
                else:
                    print(f"Could not replace node {node}")

    def add_transaction(self, sender, reciever, amount):
        self.transactions.append({
            "sender": sender,
            "reciever": reciever,
            "amount": amount
        })

        print("transaction created: ", self.transactions)
        return self.len + 1

    def discover_nodes(self, port: str):
        nodes = [f'127.0.0.1:{port}']
        traversed = nodes.copy()
        while len(nodes):
            node = nodes.pop()
            print(f"Printing node {node}")
            response = requests.get(f"http://{node}/nodes").json()
            n = response["nodes"]
            print(n)
            for i in n:
                if i not in traversed:
                    print(f"Appending {i}")
                    traversed.append(i)
                    nodes.append(i)
        return traversed

    def add_node(self, address: str):
        print(f"{address}")
        if urlparse(address).netloc not in self.nodes:
            if address.endswith(str(self.port)):
                return
            print(f"adding {address}")
            self.nodes.add(urlparse(address).netloc)
            response = requests.post(f"{address}/add_node", json={
                "nodes": [f"http://127.0.0.1:{self.port}"]
            })
            print(response)
        print("nodes: ", self.nodes)
        self.replace_chain()

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        nodes_to_remove = []
        for node in network:
            try:
                response = requests.get(f"http://{node}/chain")
                if response.status_code == 200:
                    result = response.json()
                    chain = result["chain"]

                    length = result["length"]
                    valid = self.is_chain_valid(chain)

                    if length > max_length and valid:
                        print(f"Found chain at {node}")
                        longest_chain = chain
                        max_length = length
            except Exception as e:
                print("Error connecting to node, removing it...")
                nodes_to_remove.append(node)
                continue

        for node in nodes_to_remove:
            self.nodes.discard(node)

        if longest_chain:
            self.len = max_length
            self.chain = longest_chain
            return True
        return False

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof) -> str:
        new_proof = 1
        validate = "0"*self.pow
        while True:
            hash_op = hashlib.sha256(
                str(new_proof**2 - prev_proof**2).encode()).hexdigest()

            if hash_op[:self.pow] == validate:

                return new_proof
            new_proof += 1

    def hash(Self, block) -> str:
        enc_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(enc_block).hexdigest()

    def is_chain_valid(self, chain) -> bool:
        prev_block = chain[0]
        for block in chain[1:]:
            if block["prev_hash"] != self.hash(prev_block):
                print("------------Prev hash is invalid------------")
                print(block["prev_hash"])
                print(self.hash(prev_block))
                return False
            prev_proof = prev_block["proof"]
            curr_proof = block["proof"]
            hash_op = hashlib.sha256(
                str(curr_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_op[:4] != "0000":
                print("----------PoW is not Valid----------")
                return False
            prev_block = block

        return True
