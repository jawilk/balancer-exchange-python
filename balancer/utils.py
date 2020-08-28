import json


def load_abi(path):
    with open(path) as f:
        contract_abi = json.load(f)
    return contract_abi
