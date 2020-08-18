# Attempt to find good prices within Uniswap
import time
from web3 import Web3
from uniswap import Uniswap
import utils  # Throws error. Need to check how to import appropriately!

##############################---WEB3---#######################################
secrets = utils.getJSONinfo("Secrets.txt")
infura_url = f"https://mainnet.infura.io/v3/{secrets['INFURA_KEY']}"
web3 = Web3(Web3.HTTPProvider(infura_url))
assert web3.isConnected(), "Not connected to ETH node in INFURA"

#############################---UNISWAP---#####################################
uniswap_v1 = Uniswap(
    address="0x5222ffb580f1253234d616A991c23295742A4704",
    private_key=secrets['PRIVATE_KEY'],
    web3=web3,
    version=1,
)

uniswap_v2 = Uniswap(
    address="0x5222ffb580f1253234d616A991c23295742A4704",
    private_key=secrets['PRIVATE_KEY'],
    web3=web3,
    version=2,
)

#############################---TOKENS---######################################
tokens = utils.getJSONinfo("Tokens.txt")
blacklist = ["eth", "weth", "bzrx", "bal"]  # Note that ETH and WETH are == ETH

# These tokens give different problems.
# weth = ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "Wrapped Ether"]  # !!!NW
# bzrx = ["0x56d811088235F11C8920698a204A5010a788f4b3", "bZx Protocol Token"] !!!NW
# bal = ["0xba100000625a3754423978a60c9317c58a424e3D", "BAL Balancer"] !!!NW

############################---ARBITRAGE---####################################
# TODO: Would be useful to know transaction fee costs at the time
time_start = time.time()

# amount = 1*10**18  #1 eth
amount = 1 * 10 ** 17

for token_key in tokens:
    if token_key not in blacklist:
        _token_address = tokens[token_key][0]
        _token_id = tokens[token_key][1]

        print(f"\nFinding arbitrage for {token_key}:{_token_id} at {_token_address}")
        # BUY IN V1, SELL IN V2
        take_v1 = uniswap_v1.get_eth_token_input_price(_token_address, amount)
        give_v2 = uniswap_v2.get_token_eth_input_price(_token_address, take_v1)
        # BUY IN V2, SELL IN V1
        take_v2 = uniswap_v2.get_eth_token_input_price(_token_address, amount)
        give_v1 = uniswap_v1.get_token_eth_input_price(_token_address, take_v2)

        if give_v2 > amount:
            print(
                f"Worth! Spend {web3.fromWei(amount, 'ether')} ETH in  {_token_id} in V1, and sell it in V2. Profit = {web3.fromWei(give_v2 - amount, 'ether')} ETH \n"
            )

        if give_v1 > amount:
            print(
                f"Worth! Spend {web3.fromWei(amount, 'ether')} ETH in  {_token_id} in V2, and sell it in V1. Profit = {web3.fromWei(give_v1 - amount, 'ether')} ETH \n"
            )


time_elapsed = round(time.time() - time_start, 2)
print(f"Program time: {time_elapsed} seconds")
