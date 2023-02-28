from flask import Flask, jsonify
import blockchain

chain = blockchain.Blockchain()
print(chain)

app = Flask(__name__)


@app.route('/mine', methods=["GET"])
def mine():
    # print(chain)
    prev_block = chain.get_prev_block()
    prev_proof = prev_block["proof"]
    proof = chain.proof_of_work(prev_proof)
    prev_hash = chain.hash(prev_block)
    block = chain.create_block(proof, prev_hash)
    response = {
        "msg": "Success",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "prev_hash": block["prev_hash"]
    }

    return jsonify(response), 200


@app.route('/chain', methods=["GET"])
def get_chain():
    response = chain.chain

    return jsonify(response)


@app.route('/valid', methods=["GET"])
def is_valid():
    response = {
        "valid": chain.is_chain_valid()
    }

    return jsonify(response)
