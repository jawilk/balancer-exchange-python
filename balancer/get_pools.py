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
