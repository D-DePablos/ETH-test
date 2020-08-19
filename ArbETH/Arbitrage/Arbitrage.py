# Attempt to find good prices within Uniswap
import os, sys
import time
from web3 import Web3
from uniswap import Uniswap

# Hack to get imports to work
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Utils import utils

#############################---SECRETS---######################################
# Load in relevant json file
try:
    secrets = utils.getJSONinfo("Secrets.json")
except FileNotFoundError:
    raise Exception("Secrets.json file not found. Have you run SetupFiles.py?")

# These properties can be more or less depending on individual needs
infura_key = secrets["INFURA_KEY"]
wallet_name = secrets["WALLET_NAME"]
wallet_address = secrets["WALLET_ADDRESS"]
private_key = secrets["PRIVATE_KEY"]

print(f"Using {wallet_name}, with a public address of {wallet_address}")

##############################---WEB3---#######################################
infura_url = f"https://mainnet.infura.io/v3/{infura_key}"
web3 = Web3(Web3.HTTPProvider(infura_url))
assert web3.isConnected(), "Not connected to ETH node in INFURA"

#############################---UNISWAP---#####################################
uniswap_v1 = Uniswap(
    address=wallet_address,
    private_key=private_key,
    web3=web3,
    version=1,
)

uniswap_v2 = Uniswap(
    address=wallet_address,
    private_key=private_key,
    web3=web3,
    version=2,
)

#############################---TOKENS---######################################
tokens = utils.getJSONinfo("Tokens.json")
blacklist = ["eth", "weth", "bzrx", "bal"]  # Note that ETH and WETH are == ETH

# These tokens give different problems.
# ["bzrx", "bal"]

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
        _take_v1 = uniswap_v1.get_eth_token_input_price(_token_address, amount)
        _give_v2 = uniswap_v2.get_token_eth_input_price(_token_address, _take_v1)

        # BUY IN V2, SELL IN V1
        _take_v2 = uniswap_v2.get_eth_token_input_price(_token_address, amount)
        _give_v1 = uniswap_v1.get_token_eth_input_price(_token_address, _take_v2)

        if _give_v2 > amount:
            print(
                f"Worth! Spend {web3.fromWei(amount, 'ether')} \
                 ETH in  {_token_id} in V1, and sell it in V2. \
                 Profit = {web3.fromWei(_give_v2 - amount, 'ether')} ETH \n"
            )

        if _give_v1 > amount:
            print(
                f"Worth! Spend {web3.fromWei(amount, 'ether')} \
                 ETH in  {_token_id} in V2, and sell it in V1.  \
                 Profit = {web3.fromWei(_give_v1 - amount, 'ether')} ETH \n"
            )


time_elapsed = round(time.time() - time_start, 2)
print(f"Program time: {time_elapsed} seconds")