import json

from web3 import Web3

import keys

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+keys.INFURA_ID))

class BalancerPool():
    ''' https://docs.balancer.finance/smart-contracts/api '''
    ABI_PATH = 'abi/BPool.abi'

    def __init__(self, contract_address):
        self.contract_address = contract_address
        self.contract_abi = self._load_abi()
        self.contract = w3.eth.contract(
                            address=self.contract_address,
                            abi=self.contract_abi,
                        )

        # Pool properties
        self.bone = self.get_bone()
        self.fee = self.get_swap_fee()
        self.num_tokens = self.get_num_tokens()
        

    def _load_abi(self):
        with open(self.ABI_PATH) as f:
            contract_abi = json.load(f)
        return contract_abi

    def get_bone(self):
        return self.contract.functions.BONE().call()

    def get_swap_fee(self):
        return self.contract.functions.getSwapFee().call()

    def get_num_tokens(self):
        return self.contract.functions.getNumTokens().call()

    def get_final_tokens(self):
        return self.contract.functions.getFinalTokens().call()

    def get_normalized_weight(self, address):
        return self.contract.functions.getNormalizedWeight(address).call() / 10**16

    def get_spot_price(self, address_in, address_out):
        return self.contract.functions.getSpotPrice(address_in, address_out).call()
        

weth_bal = BalancerPool('0x59A19D8c652FA0284f44113D0ff9aBa70bd46fB4')
print(weth_bal.get_final_tokens())
print(weth_bal.get_normalized_weight(weth_bal.get_final_tokens()[0]))
