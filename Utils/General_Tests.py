import json
from web3 import Web3


def getJSONinfo(file):
    """
    Get Information from a json file within Utils directory
    """
    with open(f"Utils/{file}", "r") as openfile:
        JSONinfo = json.load(openfile)

    return JSONinfo


# Secrets Handling -> Set INFURA KEY from FileGeneration.ipynb
try:
    secrets = getJSONinfo("Secrets.json")
except FileNotFoundError:
    raise Exception(
        "Not found Secrets.json file. Are you sure you have run SetupFiles.py?"
    )

# Web3 provider from Infura (ACCOUNT SPECIFIC)
w3_main = f"https://mainnet.infura.io/v3/{secrets['INFURA_KEY']}"
w3_test = f"https://ropsten.infura.io/v3/{secrets['INFURA_KEY']}"


# Open up a specific ETH wallet
Wallet_address = secrets["WALLET_ADDRESS"]

# Quick test of a web3 connection
def test_connection(connection):
    """
    Prints diagnostic information from ETH blockchain
    """
    if connection.isConnected():
        print("Successfully connected to ETH network.")
        print(f"Blocknumber: {connection.eth.blockNumber} ")
    else:
        raise Exception("Not connected to ETH network.")


if __name__ == "__main__":

    # Select testnet or mainnet
    web3 = Web3(Web3.HTTPProvider(w3_main))
    test_connection(web3)
    balance = web3.fromWei(web3.eth.getBalance(Wallet_address), "ether")
    print(balance)
