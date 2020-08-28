# balancer-exchange-python
Unofficial Python wrapper for balancer.exchange, for pools see https://pools.balancer.exchange/#/.
Depends on web3 and graphql, infura key is needed.

## Examples
```python
from web3 import Web3

from balancer import Pool
import keys


w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+keys.INFURA_ID))


weth_bal = Pool(w3, '0x59A19D8c652FA0284f44113D0ff9aBa70bd46fB4')
print(weth_bal.final_tokens())
print(weth_bal.get_normalized_weight(weth_bal.final_tokens()[0]))
```

Get all pools with BAL token (in first 100):

```python
from gql import gql, Client, AIOHTTPTransport
from web3 import Web3

from balancer import Pool
import keys


w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+keys.INFURA_ID))


transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/balancer-labs/balancer")

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql(
    """
  {
  pools(first: 100, where: {publicSwap: true}) {
    id
    finalized
    publicSwap
    swapFee
    totalWeight
    tokensList
    tokens {
      id
      address
      balance
      decimals
      symbol
      denormWeight
    }
  }
}

"""
)

pools = client.execute(query)
pools = pools['pools'] 

all_pools = []
for pool in pools:
    all_pools.append(Pool(
        w3=w3,
        contract_address = Web3.toChecksumAddress(pool['id']),
        finalized = pool['finalized'],
        public_swap = pool['publicSwap'],
        swap_fee = pool['swapFee'],
        total_weight = pool['totalWeight'],
        tokens_list = pool['tokensList'],
        tokens = pool['tokens'],
    ))


bal_pools = []
for pool in all_pools:
    for token in pool.final_tokens():
        if token.symbol == 'BAL':
            bal_pools.append(pool)
            break

for count, bal_pool in enumerate(bal_pools):
    print(f'BAL pool {count}:', bal_pool.contract_address)
```

Gives

BAL pool 0: 0x01cA3f774742E0b12E232A9004FA698f45EF04A7              
BAL pool 1: 0x05eefA2a20b39dFE8A167Ed0850E5590aa880Fe1                
BAL pool 2: 0x060feb082A4AA0424b8fF4FDb769FaF9E06e1Fb9               
BAL pool 3: 0x06BcDfFf7B51f5e67f44403aE0C2EE1A1A8F6E28         
BAL pool 4: 0x075b5B7cbC3AddB9D8Ce86629CEb066DA8617BB0         
BAL pool 5: 0x07B18C2686F3d1BA0Fa8C51edc856819f2b1100A      
BAL pool 6: 0x08a2f472096848AE465055cAa14FdaB94679e000       
BAL pool 7: 0x097DB362F672832d27E52C3c3F97D3B0D442abd2    
BAL pool 8: 0x0983Ca5edE50074AC268583E740DC14BD77af8c0         
BAL pool 9: 0x102Efb11d588Fa03dfC9Fb5E0894Dd241839D3f8        
