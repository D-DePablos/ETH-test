from web3 import Web3
import utils

# Secrets Handling -> Set INFURA KEY from FileGeneration.ipynb
secrets = utils.getJSONinfo('Secrets.txt')

# Web3 provider from Infura (ACCOUNT SPECIFIC)
w3_main =  f"https://mainnet.infura.io/v3/{secrets['INFURA_KEY']}"
w3_test =  f"https://ropsten.infura.io/v3/{secrets['INFURA_KEY']}"


# Open up a specific ETH wallet
wallet = utils.getJSONinfo('Wallets.txt')
Dapper_Wallet = wallet["Dapper"]

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


if __name__ == '__main__':

    # Select testnet or mainnet
    web3 = Web3(Web3.HTTPProvider(w3_main))
    test_connection(web3)
    balance = web3.fromWei(web3.eth.getBalance(Dapper_Wallet), 'ether')
    print(balance)