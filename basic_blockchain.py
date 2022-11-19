# Create a Blockchain class
# To be installed:
# It may raise an error when using last version libraries, it works fine with Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = [] # Create the chain
        self.create_block(proof = 1, previous_hash = '0') # Create the genesis block

    def create_block(self, proof, previous_hash): # Create a block
        block = {'index': len(self.chain) + 1, # Index of the block
                 'timestamp': str(datetime.datetime.now()), # Timestamp of the block
                 'proof': proof, # Proof of work
                 'previous_hash': previous_hash} # Previous hash
        self.chain.append(block) # Append the block to the chain
        return block 

    def get_previous_block(self): # Get the previous block
        return self.chain[-1]

    def proof_of_work(self, previous_proof): # Proof of work
        new_proof = 1 
        check_proof = False 
        while check_proof is False: # While the proof is not valid
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # Hash the proof
            if hash_operation[:4] == '0000': # If the hash starts with 4 zeros
                check_proof = True # The proof is valid
            else:
                new_proof += 1 # If the proof is not valid, increment the proof
        return new_proof
    
    def hash(self, block): # Hash the block
        encoded_block = json.dumps(block, sort_keys = True).encode() # Encode the block
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain): # Check if the chain is valid
        previous_block = chain[0] 
        block_index = 1
        while block_index < len(chain): # While the block index is less than the length of the chain
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block): # If the previous hash is not equal to the hash of the previous block
                return False
            previous_proof = previous_block['proof'] # Get the proof of the previous block
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() # Hash the proof
            if hash_operation[:4] != '0000': # If the hash does not start with 4 zeros
                return False
            previous_block = block # Set the previous block to the current block
            block_index += 1 # Increment the block index
        return True

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET']) # Get request
def mine_block(): # Mine a block
    previous_block = blockchain.get_previous_block() # Get the previous block
    previous_proof = previous_block['proof'] # Get the proof of the previous block
    proof = blockchain.proof_of_work(previous_proof) # Get the proof of work
    previous_hash = blockchain.hash(previous_block) # Get the hash of the previous block
    block = blockchain.create_block(proof, previous_hash) # Create a block
    response = {'message': 'Congratulations, you just mined a block!', # Response
                'index': block['index'], # Index of the block
                'timestamp': block['timestamp'], # Timestamp of the block
                'proof': block['proof'], # Proof of work
                'previous_hash': block['previous_hash']} # Previous hash
    return jsonify(response), 200 # Return the response

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET']) # Get request
def get_chain(): # Get the chain
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)} # Length of the chain
    return jsonify(response), 200 

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain) # Check if the chain is valid
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000) # Run the app on port 5000
