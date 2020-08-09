# Following https://web3py.readthedocs.io/en/latest/quickstart.html
from web3 import Web3

# Manual setup of web3 provider from INfura (need to register)
w3_main =  "https://mainnet.infura.io/v3/c65dc98caf2a4466b2f642011705d15f"
w3_test =  "https://ropsten.infura.io/v3/c65dc98caf2a4466b2f642011705d15f"

# Select testnet or mainnet
w3 = Web3(Web3.HTTPProvider("w3_test"))

def test_connection(w3connection):
    """
    Prints diagnostic information from ETH blockchain
    """
    print(f"{w3.isConnected()}: Currently connected to ETH network")

def CreateContract():
    assert(w3.isConnected), "Not Connected to a valid web3 provider"


if __name__ == '__main__':
    pass