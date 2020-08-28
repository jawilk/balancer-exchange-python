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
    ):
        self.contract_address = contract_address
        self.contract_abi = load_abi(self.ABI_PATH)
        self.contract = w3.eth.contract(
                            address=self.contract_address,
                            abi=self.contract_abi,
                        )

        # Pool properties
        self.properties = {
            'isFinalized': finalized,
            'isPublicSwap': public_swap,
            'getSwapFee': swap_fee,
            'getTotalDenormalizedWeight': total_weight,
            'tokens_list': tokens_list,
            'getFinalTokens': initialize_tokens(tokens) if tokens else None,
        }

    def _set_value(self, prop, *argv):
        if argv:
            self.properties[prop] = self.properties[prop] if self.properties.get(prop) else self.contract.get_function_by_name(prop)(*argv).call()
            return self.properties[prop]
        self.properties[prop] = self.properties[prop] if self.properties.get(prop) else self.contract.get_function_by_name(prop)().call()
        return self.properties[prop]

    def bone(self):
        return self._set_value('BONE')

    def bpow_precision(self):
        return self._set_value('BPOW_PRECISION')

    def exit_fee(self):
        return self._set_value('EXIT_FEE')

    def init_pool_supply(self):
        return self._set_value('INIT_POOL_SUPPLY')

    def max_bound_tokens(self):
        return self._set_value('MAX_BOUND_TOKENS')

    def max_bpow_base(self):
        return self._set_value('MAX_BPOW_BASE')

    def max_fee(self):
        return self._set_value('MAX_FEE')

    def max_in_ratio(self):
        return self._set_value('MAX_IN_RATIO')

    def max_out_ratio(self):
        return self._set_value('MAX_OUT_RATIO')

    def max_total_weight(self):
        return self._set_value('MAX_TOTAL_WEIGHT')

    def max_weight(self):
        return self._set_value('MAX_WEIGHT')

    def min_balance(self):
        return self._set_value('MIN_BAlANCE')

    def min_bound_tokens(self):
        return self._set_value('MIN_BOUND_TOKENS')

    def min_bpow_base(self):
        return self._set_value('MIN_BPOW_BASE')

    def min_fee(self):
        return self._set_value('MIN_FEE')

    def min_weight(self):
        return self._set_value('MIN_WEIGHT')

    def allowance(self, src_address, dst_address):
        return self._set_value('ALLOWANCE', src_address, dst_address)

    def balance_of(self, address):
        return self._set_value('BALANCE_OF', address)

    def decimals(self):
        return self._set_value('decimals')

    def color(self):
        return self._set_value('getColor')

    def controller(self):
        return self._set_value('getController')

    def final_tokens(self):
        return self._set_value('getFinalTokens')

    def swap_fee(self):
        return self._set_value('getSwapFee')

    def total_denormalized_weight(self):
        return self._set_value('getTotalDenormalizedWeight')

    def is_finalized(self):
        return self._set_value('isFinalized)

    def is_public_swap(self):
        return self._set_value('isPublicSwap')

    def name(self):
        return self._set_value('name')

    def symbol(self):
        return self._set_value('symbol')

    def total_supply(self):
        return self._set_value('totalSupply')

    def calc_in_given_out(self, *argv):
        '''argv:
           tokenBalanceIn
           tokenWeightIn
           tokenBalanceOut
           tokenWeightOut
           tokenAmountOut
           swapFee
        '''
        return self.contract.functions.calcInGivenOut(*argv).call()

    def calc_out_given_in(self, *argv):
        '''argv:
           tokenBalanceIn
           tokenWeightIn
           tokenBalanceOut
           tokenWeightOut
           tokenAmountIn
           swapFee
        '''
        return self.contract.functions.calcOutGivenIn(*argv).call()

    def calc_pool_in_given_single_out(self, *argv):
        '''argv:
           tokenBalanceOut
           tokenWeightOut
           poolSupply
           totalWeight
           tokenAmountOut
           swapFee
        '''
        return self.contract.functions.calcPoolInGivenSingleOut(*argv).call()

    def calc_pool_out_given_single_in(self, *argv):
       '''argv:
           tokenBalanceIn
           tokenWeightIn
           poolSupply
           totalWeight
           tokenAmountIn
           swapFee
        '''
        return self.contract.functions.calcPoolOutGivenSingleIn(*argv).call()

    def calc_single_in_given_pool_out(self, *argv):
        '''argv:
           tokenBalanceIn
           tokenWeightIn
           poolSupply
           totalWeight
           tokenAmountOut
           swapFee
        '''
        return self.contract.functions.calcSingleInGivenPoolOut(*argv).call()

    def calc_single_out_given_pool_in(self, *argv):
        '''argv:
           tokenBalanceOut
           tokenWeightOut
           poolSupply
           totalWeight
           poolAmountIn
           swapFee
        '''
        return self.contract.functions.calcPoolOutGivenSingleIn(*argv).call()

    def cal_spot_price(self, *argv):
        '''argv:
           tokenBalanceIn
           tokenWeightIn
           tokenBalanceOut
           tokenWeightOut
           swapFee
        '''
        return self.contract.functions.calcSpotPrice(*argv).call()

    def get_balance(self, address):
        return self.contract.functions.getBalance(address).call()

    def get_denormalized_weight(self, token_address):
        return self.contract.functions.getDenormalizedWeight(token_address).call()

    def get_normalized_weight(self, token_address):
        return self.contract.functions.getNormalizedWeight(token_address).call() #/ 10**16

    def get_num_tokens(self):
        return self.contract.functions.getNumTokens().call()

    def get_spot_price(self, token_in_address, token_out_address):
        return self.contract.functions.getSpotPrice(token_in_address, token_out_address).call()

    def get_spot_price_sans_fee(self, token_in_address, token_out_address):
        return self.contract.functions.getSpotPriceSansFee(token_in_address, token_out_address).call()

    def is_bound(self, token_address):
        return self.contract.functions.isBound(token_address).call()
