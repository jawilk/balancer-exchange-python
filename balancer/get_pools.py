from gql import gql, Client, AIOHTTPTransport
from web3 import Web3

from balancer import Pool


transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/balancer-labs/balancer")

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql(
    """
  {
  pools(first: 1, where: {publicSwap: true}) {
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
        contract_address = Web3.toChecksumAddress(pool['id']),
        address_only = False,
        finalized = pool['finalized'],
        public_swap = pool['publicSwap'],
        swap_fee = pool['swapFee'],
        total_weight = pool['totalWeight'],
        tokens_list = pool['tokensList'],
        tokens = pool['tokens'],
    ))

print(all_pools[0].tokens[0].symbol)
