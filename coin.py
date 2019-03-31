import hashlib
import json
import os
from time import time

COIN_DIR = os.curdir + '/coins/'

def check_coin(index):
    current_index = str(index)
    previous_index = str(int(index) - 1)
    current_proof = -1
    current_hash = 0
    previous_hash = 0
    temp = {'coin' : '', 'result' : '', 'proof': ''}
    
    try:
        file_dict = json.load(open(COIN_DIR + current_index + '.json'))
        current_hash = file_dict['previous_hash']
        current_proof = file_dict['proof']
    except Exception as exception:
        print(exception)
    
    try:
        previous_hash = hashlib.sha256(open(COIN_DIR + previous_index + '.json', 'rb').read()).hexdigest()
    except Exception as exception:
        print(exception)
    
    temp['coin'] = previous_index
    temp['proof'] = current_proof
    
    if current_hash == previous_hash:
        temp['result'] = 'Ok'
    else:
        temp['result'] = 'Error'
    
    return temp

def check_coins_integrity():
    result = []
    index = int(get_next_coin)
    
    for i in range(2, index):
        check_coin(index)
        result.append(temp)
   
    return result


def hash_coin(file_name):
    file_name = str(file_name)
    
    if not file_name.endswith('.json'):
        file_name += '.json'
    
    try:
        with open(COIN_DIR + file_name, 'rb') as file:
            return hashlib.sha256(file.read()).hexdigest()
    except Exception as exception:
        print('File "'+file_name+'" does not exist!n', exception)


def get_next_coin():
    files = os.listdir(COIN_DIR)
    index_list = [int(file.split('.')[0]) for file in files]
    current_index = sorted(index_list)[-1]
    next_index = current_index + 1
    
    return str(next_index)


def is_valid_proof(last_proof, proof, difficulty):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    
    return guess_hash[:difficulty] == '0' * difficulty


def proof_of_work(file_name, difficulty = 1):
    file_name = str(file_name)
    
    if file_name.endswith('.json'):
        file_name = int(file_name.split('.')[0])
    else:
        file_name = int(file_name)

    last_proof = json.load(open(COIN_DIR + str(file_name - 1) + '.json'))['proof']
    proof = 0
    
    while is_valid_proof(last_proof, proof, difficulty) is False:
        proof += 1
    
    current_coin = json.load(open(COIN_DIR + str(file_name) + '.json'))
    current_coin['proof'] = proof
    current_coin['previous_hash'] = hash_coin(str(file_name - 1))
    
    with open(COIN_DIR + str(file_name) + '.json', 'w') as file:
        json.dump(current_coin, file, indent=4, ensure_ascii=False)


def write_coin(make_proof=False):
    current_index = get_next_coin()
    previous_index = str(int(current_index) - 1)
    prev_coin_hash = hash_coin(previous_index)
    data = {
            'previous_hash' : prev_coin_hash,
            'timestamp' : time(),
            'proof' : -1,
            'index' : current_index
            }

    with open(COIN_DIR + current_index + '.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    if make_proof is True:
        proof_of_work(str(current_index))


if __name__ == '__main__':
    print(check_coins_integrity())
