from uuid import uuid4
from flask import Flask, jsonify, request
import blockchain, requests


app = Flask(__name__)

node_address = str(uuid4()).replace("-", "")

@app.route('/mine', methods=["GET"])
def mine():
    block = chain.mine_block(node_address, "Myself")
    response = {
        "msg": "Success",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "prev_hash": block["prev_hash"],
        "transactions": block["transactions"]
    }

    return jsonify(response), 200


@app.route('/chain', methods=["GET"])
def get_chain():
    response = {
        "chain" : chain.chain,
        "length": chain.len
        }

    return jsonify(response)


@app.route('/valid', methods=["GET"])
def is_valid():
    response = {
        "valid": chain.is_chain_valid(chain.chain)
    }

    return jsonify(response)


@app.route('/add_transaction', methods=["POST"])
def add_transaction():
    json = request.get_json()
    transaction_keys = ["sender", "reciever", "amount"]
    if not all( key in json for key in transaction_keys):
        return "Some elements are missing", 400
    
    idx = chain.add_transaction(json["sender"], json["reciever"], json["amount"])

    response = {
        "message": f"Trans created at idx {idx}"
    }

    return jsonify(response), 201


@app.route('/add_node', methods=["POST"])
def add_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if not nodes:
        return "No nodes", 400
    for node in nodes:
        chain.add_node(node)

    response = {
        "message": "Success",
        "Nodes": list(chain.nodes)
    }

    return jsonify(response), 201

# @app.route('/discover', methods=["POST"])
# def discover():
#     json = request.get_json()
#     sender = json.get('sender')
    
#     nodes = chain.discover_nodes(sender)
    
#     response = {
#         "message": "Success",
#         "nodes": list(nodes)
#     }

#     return jsonify(response), 201
    

@app.route('/discover', methods=["GET"])
def discover():
    nodes = chain.discover_nodes(port)
    
    return jsonify(nodes), 200


@app.route('/replace', methods=["GET"])
def replace_chain():
    is_chain_replaced = chain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'There is a bigger chain',
                    'chain': chain.chain}
    else:
        response = {'message': 'Longest chain',
                    'chain': chain.chain}
    return jsonify(response), 200

@app.route('/nodes', methods=["GET"])
def get_nodes():
    response = {
        "nodes": list(chain.nodes)
    }
    return jsonify(response), 200
if __name__ == "__main__":
    port = int(input("Enter port number: "))
    chain = blockchain.Blockchain(port)
    app.run(port=port ,debug=False)
