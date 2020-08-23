from os import getcwd
import json
import requests
from web3 import Web3


class UniversalHandler():
    """
    Class that handles all common properties
    """
    def __init__(self, fromToken, toToken, amount):

        # Read in top
        self.fromToken = fromToken
        self.toToken = toToken
        self.amount = amount  # In the token itself? -> Would be good to be in ETH
        self.amount_wei = Web3.toWei(amount, "ether")

        # Placeholders for future properties
        self.exchange = None
        self.objective_amount = None
        self.objective_amount_wei = None

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
        # Prepare the token list location
        tokenlist_location = f"{getcwd()}/REST_API/1inchtokens.json"

        # Get token list
        req = requests.get("https://api.1inch.exchange/v1.1/tokens")

        if req.status_code !=200:
            raise ValueError(f"Bad Http response {req.status_code}")

        with open(tokenlist_location, "w") as json_file:
            json.dump(req.json(), json_file, indent = 4, sort_keys=True)
        print(f"Updated token list at {tokenlist_location}")

        return tokenlist_location 

    def quotePrice(self, disabledExchanges=None):
        """
        Quote Price function, returns a json with:

        Returns within json:
        ####################################################################
        fromToken: from Token with {"symbol", "name", "decimals", "address"}
        toToken: to Token with {"symbol", "name", "decimals", "address"}
        toTokenAmount: How much of toToken you get {amount}
        fromTokenAmount: Amount of tojens for swap {amount}
        exchanges: Name and percentage of exchange used {{"name":XXX}, {"part":percentage}}
        ####################################################################
        """

        # Set the endpoint
        endpoint = f"https://api.1inch.exchange/v1.1/"\
        f"quote?fromTokenSymbol={self.fromToken}"\
        f"&toTokenSymbol={self.toToken}&amount={self.amount_wei}"

        # If ignoring some exchanges
        if disabledExchanges is not None:
            endpoint += "&disabledExchangesList="
            for exchange in disabledExchanges:
                endpoint += f"{exchange},"

        # Generate the request and check that it passed with 200
        req = requests.get(endpoint)

        if req.status_code !=200:
            raise ValueError(f"Bad Http response {req.status_code}") 

        # Response object
        jsonResponse = req.json()
        self.objective_amount_wei = jsonResponse["toTokenAmount"]
        print(Web3.fromWei(float(self.objective_amount_wei), "ether"))
        self.objective_amount = float(Web3.fromWei(float(self.objective_amount_wei), "ether"))

        # Pick out the exchange which uses 100 %
        _exchangeAllocations = jsonResponse["exchanges"]

        # Requires 100 % of the trade in one exchange
        usedExchanges = next((sub for sub in _exchangeAllocations if sub['part'] == 100), None)  

        try:
            self.exchange = usedExchanges["name"]
        except KeyError:
            raise KeyError("Unable to find an exchange with"\
                           f"100% liquidity available. Check list {_exchangeAllocations}")

        return(self.exchange, self.objective_amount)


    def swap(
        self, 
        fromAddress, 
        disabledExchanges=None, 
        referrerAddress=None,
        max_slippage=3, 
        fee=None,
        gasPrice=None):
        """
        Get swap call data for aggregated swap
        (which can be used with web3 provider to send transaction)

        Parameters:

        :param fromAddress: Address which will perform transaction
        :param disabledExchanges: (Optional) - Whether to disable exchanges
        :param referrerAddress: (Optional) - If using referral address (e.g for production)
        :param max_slippage: (Optional, defaults to 1%) - Max slippage allowed
        :param fee: (Optional) - Max loss in transformation
        :param gasPrice: (Optional) - If want to use specific gas price

        """

        # Set the endpoint
        endpoint = "https://api.1inch.exchange/v1.1/"\
            f"swap?fromTokenSymbol={self.fromToken}&toTokenSymbol={self.toToken}"\
                f"&amount={self.amount_wei}"\
                   f"&fromAddress={fromAddress}"\
                       f"&slippage={max_slippage}"\
                           "&disableEstimate=true"

        # If ignoring some exchanges
        if disabledExchanges is not None:
            endpoint += "&disabledExchangesList="
            for exchange in disabledExchanges:
                endpoint += f"{exchange},"

        # Test referral
        if referrerAddress is not None:
            endpoint += f"&referrerAddress={referrerAddress}"

        # Max Fees to pay (optional)
        if fee is not None:
            endpoint += f"&fee={fee}"

        # Gas price -> Implement here if any pointer to current price
        if gasPrice is not None:
            endpoint += f"&gasPrice={gasPrice}"

        # GET request and assertion of correct response
        req = requests.get(endpoint)
        if req.status_code !=200:
            raise ValueError(f"Bad Http response {req.status_code}") 

        jsonResponse = req.json()

        # TODO: Get useful parameters here

        return(jsonResponse)


if __name__ == '__main__':

    # TODO: Check this https://www.programcreek.com/python/example/107998/web3.Web3

    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from Utils import utils

    secrets = utils.getJSONinfo("Secrets.json")

    address = secrets["WALLET_ADDRESS"]

    one = oneInchHandler("DAI", "ETH", 100)
    # one.update_tokenlist()
    reqquote = one.quotePrice(disabledExchanges=['Uniswap', 'AirSwap'])
    print(reqquote)

    reqswap = one.swap(fromAddress=address)
    print(reqswap)
