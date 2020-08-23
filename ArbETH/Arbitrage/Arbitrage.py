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
blacklist = ["ETH", "WETH", "BZRX", "BAL"]  # Note that ETH and WETH are == ETH

# These tokens give different problems.
# ["BZRX", "BAL"]

############################---ARBITRAGE---####################################
# TODO: Would be useful to know transaction fee costs at the time
time_start = time.time()

<<<<<<< HEAD
<<<<<<< HEAD
# amount = 1*10**18  #1 eth
amount = 1 * 10 ** 17
=======
=======
>>>>>>> 78765717970f10cf661f5d6142662e1eb122eed6
# 1*10**18 = 1 eth
invest = 1 * 10 ** 17
profit = 0
ex_tax = 0.003
fl_tax = 0.0009
<<<<<<< HEAD
>>>>>>> 7876571... Included Flash Loan Fees (first versions of fees)
=======
>>>>>>> 78765717970f10cf661f5d6142662e1eb122eed6

for token_key in tokens:
    if token_key not in blacklist:
        _token_address = tokens[token_key][0]
        _token_id = tokens[token_key][1]
        print(f"\nFinding arbitrage for {token_key}:{_token_id} at {_token_address}")

<<<<<<< HEAD
<<<<<<< HEAD
        if _give_v2 > amount:
=======
=======
>>>>>>> 78765717970f10cf661f5d6142662e1eb122eed6
        # Flash Loan Fee
        _fl_fee = int(invest*fl_tax)
        # First Trade Fee
        _fee = int(invest*ex_tax)
        _remaining = invest - _fee

        ##### EXCHANGE 1: BUY IN V1, SELL IN V2
        _take_v1 = uniswap_v1.get_eth_token_input_price(_token_address, _remaining)
        # Second Trade Fee
        _fee = int(_take_v1*ex_tax)
        _remaining_1 = _take_v1 - _fee
        # Second Trade
        _give_v2 = uniswap_v2.get_token_eth_input_price(_token_address, _remaining_1)
        _give_v2 = _give_v2 - _fl_fee

        ##### EXCHANGE 2: BUY IN V2, SELL IN V1
        _take_v2 = uniswap_v2.get_eth_token_input_price(_token_address, _remaining)
        # Second Trade Fee
        _fee = int(_take_v2*ex_tax)
        _remaining_2 = _take_v2 - _fee
        # Second Trade
        _give_v1 = uniswap_v1.get_token_eth_input_price(_token_address, _remaining_2)
        _give_v1 = _give_v1 - _fl_fee

        if _give_v2 > invest:
<<<<<<< HEAD
>>>>>>> 7876571... Included Flash Loan Fees (first versions of fees)
=======
>>>>>>> 78765717970f10cf661f5d6142662e1eb122eed6
            print(
                f"Worth! Spend {web3.fromWei(invest, 'ether')} \
                 ETH in  {_token_id} in V1, and sell it in V2. \
                 Profit = {web3.fromWei(_give_v2 - invest, 'ether')} ETH \n"
            )

        if _give_v1 > invest:
            print(
                f"Worth! Spend {web3.fromWei(invest, 'ether')} \
                 ETH in  {_token_id} in V2, and sell it in V1.  \
                 Profit = {web3.fromWei(_give_v1 - invest, 'ether')} ETH \n"
            )


time_elapsed = round(time.time() - time_start, 2)
print(f"Program time: {time_elapsed} seconds")
