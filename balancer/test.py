from web3 import Web3

from balancer import Pool
import keys


w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+keys.INFURA_ID))


weth_bal = Pool(w3, '0x59A19D8c652FA0284f44113D0ff9aBa70bd46fB4')
print(weth_bal.final_tokens())
print(weth_bal.get_normalized_weight(weth_bal.final_tokens()[0]))
