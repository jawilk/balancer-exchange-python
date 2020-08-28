from gql import gql, Client, AIOHTTPTransport


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

result = client.execute(query)
print(result)
