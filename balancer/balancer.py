import json

from web3 import Web3

from utils import load_abi


def initialize_tokens(tokens):
    all_tokens = []
    for token in tokens:
        all_tokens.append(Token(
            contract_address = Web3.toChecksumAddress(token['address']),
            balance = token['balance'],
            decimals = token['decimals'],
            symbol = token['symbol'],
            denorm_weight = token['denormWeight'],
        ))
    return all_tokens

class Token:
    ''''
    tokens': [{'address': '0xa3bed4e1c75d00fa6f4e5e6922db7261b5e9acd2', 'balance':        '566201.286846114414239124', 'decimals': 18, 'denormWeight': '8', 'id': '0x003a70265a3662342010823bea15dc84c6f7ed54-0xa3bed4e1c75d00fa6f4e5e6922db7261b5e9acd2', 'symbol': 'MTA'}, {'address': '0xe2f2a5c287993345a840db3b0845fbc70f5935a5', 'balance': '783270.361777465361029266', 'decimals': 18, 'denormWeight': '2', 'id': '0x003a70265a3662342010823bea15dc84c6f7ed54-0xe2f2a5c287993345a840db3b0845fbc70f5935a5', 'symbol': 'mUSD'}]
    '''

    def __init__(
        self,
        contract_address,
        balance,
        decimals,
        symbol,
        denorm_weight,
    ):

        self.contract_address = contract_address 
        self.balance = balance
        self.decimals = decimals
        self.symbol = symbol
        self.denorm_weight = denorm_weight


class Pool:
    '''
    https://docs.balancer.finance/smart-contracts/api
    
    {'pools': [{'finalized': True, 'id': '0x003a70265a3662342010823bea15dc84c6f7ed54', 'publicSwap': True, 'swapFee': '0.001', 'tokens': [{'address': '0xa3bed4e1c75d00fa6f4e5e6922db7261b5e9acd2', 'balance': '566201.286846114414239124', 'decimals': 18, 'denormWeight': '8', 'id': '0x003a70265a3662342010823bea15dc84c6f7ed54-0xa3bed4e1c75d00fa6f4e5e6922db7261b5e9acd2', 'symbol': 'MTA'}, {'address': '0xe2f2a5c287993345a840db3b0845fbc70f5935a5', 'balance': '783270.361777465361029266', 'decimals': 18, 'denormWeight': '2', 'id': '0x003a70265a3662342010823bea15dc84c6f7ed54-0xe2f2a5c287993345a840db3b0845fbc70f5935a5', 'symbol': 'mUSD'}], 'tokensList': ['0xe2f2a5c287993345a840db3b0845fbc70f5935a5', '0xa3bed4e1c75d00fa6f4e5e6922db7261b5e9acd2'], 'totalWeight': '10'}]}
    '''
    ABI_PATH = 'abi/BPool.abi'

    def __init__(
        self,
        w3,
        contract_address,
        finalized=None,
        public_swap=None,
        swap_fee=None,
        total_weight=None,
        tokens_list=None,
        tokens=None,
        bone=None,
    ):
        self.contract_address = contract_address
        self.contract_abi = load_abi(self.ABI_PATH)
        self.contract = w3.eth.contract(
                            address=self.contract_address,
                            abi=self.contract_abi,
                        )

        # Pool properties
        self.properties = {
            'finalized': finalized,
            'public_swap': public_swap,
            'swap_fee': swap_fee,
            'total_weight': total_weight,
            'tokens_list': tokens_list,
            'getFinalTokens': initialize_tokens(tokens) if tokens else None,
            'BONE': bone,
            'getNormalizedWeight': None,
        }

    def _set_value(self, prop, *argv):
        if argv:
            self.properties[prop] = self.properties[prop] if self.properties[prop] else self.contract.get_function_by_name(prop)(*argv).call()
            return self.properties[prop]
        self.properties[prop] = self.properties[prop] if self.properties[prop] else self.contract.get_function_by_name(prop)().call()
        return self.properties[prop]

    def get_bone(self):
        return self._set_value('BONE')

    def get_num_tokens(self):
        return len(self.tokens)

    def get_final_tokens(self):
        return self._set_value('getFinalTokens')

    def get_normalized_weight(self, address):
        return self._set_value('getNormalizedWeight', address) / 10**16

    def get_spot_price(self, address_in, address_out):
        return self.contract.functions.getSpotPrice(address_in, address_out).call()
