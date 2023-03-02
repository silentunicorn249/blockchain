import blockchain, time

chain = blockchain.Blockchain()

import time

start = time.time()
# do something

for i in range(7):
    prev_block = chain.get_prev_block()
    prev_proof = prev_block["proof"]
    proof = chain.proof_of_work(prev_proof)
    prev_hash = chain.hash(prev_block)
    block = chain.create_block(proof, prev_hash)

end = time.time()
delta = end - start
print ("took %.2f seconds to process" % delta)


# exit()
for block in chain.chain:
    print(block["prev_hash"])
    print(chain.hash(block), end="\n\n")


print(chain.is_chain_valid(chain.chain))