from os import getcwd
import json
import requests
from web3 import Web3



class UniversalHandler():
    def __init__(self, fromToken, toToken, amount):
        self.fromToken = fromToken
        self.toToken = toToken
        self.amount = amount  # In the token itself? -> Would be good to be in ETH
        
        self.amount_wei = amount * 10 ** 18

    def __repr__(self):
        return(f"{self.amount} of {self.fromToken} to {self.toToken}")


class oneInchHandler(UniversalHandler):
    """
    Python Handler for 1inch.exchange
    Inherits relevant parameters from UniversalHandler
    """

    @staticmethod
    def update_tokenlist():
        """
        Update the 1inch token list in the json file
        """
        tokenlist_location = f"{getcwd()}/REST_API/1inchtokens.json"

        # Get token list
        req = requests.get("https://api.1inch.exchange/v1.1/tokens")
        assert(req.status_code == 200), f"Failed token list request with code {req.status_code}. Is the URL correct?"

        with open(tokenlist_location, "w") as json_file:
            json.dump(req.json(), json_file, indent = 4, sort_keys=True)
        print(f"Updated token list at {tokenlist_location}")

        return tokenlist_location 

    def quotePrice(self):
        """
        Quote Price function, example: 
        https://api.1inch.exchange/v1.1/quote
        ?fromTokenSymbol=ETH
        &toTokenSymbol=DAI
        &amount=100000000000000000000
        &disabledExchangesList=Bancor
        """

        endpoint = f"https://api.1inch.exchange/v1.1/quote?fromTokenSymbol={self.fromToken}&toTokenSymbol={self.toToken}&amount={self.amount_wei}"

        req = requests.get(endpoint)
        assert(req.status_code == 200), f"Failed quote with code {req.status_code}. Is the URL correct?"

        print(json.dumps(req.json(), indent=4))
    

one = oneInchHandler("DAI", "ETH", 100)
one.update_tokenlist()
one.quotePrice()

print(one)