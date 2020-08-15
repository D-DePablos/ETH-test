# Attempt to find good prices within Uniswap
import time
from web3 import Web3
from uniswap import Uniswap
import utils  # Throws error. Need to check how to import appropriately!

##############################---WEB3---#######################################
secrets = utils.getJSONinfo('Secrets.txt')
infura_url = f"https://mainnet.infura.io/v3/{secrets['INFURA_KEY']}"
web3 = Web3(Web3.HTTPProvider(infura_url))
print("Infura Connection: " + str(web3.isConnected()))

#############################---UNISWAP---#####################################
uniswap_v1 = Uniswap(address="0x5222ffb580f1253234d616A991c23295742A4704",
                          private_key="556c2c22356e68eaf82000e12ec27df2a25602787c9024418b5638cca14ecd3d",
                          web3=web3,
                          version=1)

uniswap_v2 = Uniswap(address="0x5222ffb580f1253234d616A991c23295742A4704",
                          private_key="556c2c22356e68eaf82000e12ec27df2a25602787c9024418b5638cca14ecd3d",
                          web3=web3,
                          version=2)

#############################---TOKENS---######################################
eth = ["0x0000000000000000000000000000000000000000", "ETHEREUM"]
bat = ["0x0D8775F648430679A709E98d2b0Cb6250d2887EF", "BAT"]
dai = ["0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359", "DAI Stablecoin"]

amn = ["0x737F98AC8cA59f2C68aD658E3C3d8C8963E40a4c", "AMN Amon"]
ampl = ["0xD46bA6D942050d489DBd938a2C909A5d5039A161", "AMPL Ampleforth"]
anj = ["0xcD62b1C403fa761BAadFC74C525ce2B51780b184", "ANJ AragonNetworkJuror"]
ant = ["0x960b236A07cf122663c4303350609A66A7B288C0", "ANT Aragon"]
ast = ["0x27054b13b1B798B345b591a4d22e6562d47eA75a", "AST AirSwap"]
band = ["0xBA11D00c5f74255f56a5E366F4F77f5A186d7f55", "BAND BandToken"]
bnt = ["0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C", "BNT Bancor"]


# These tokens give different problems.
#weth = ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "Wrapped Ether"]  # !!!NW
#bzrx = ["0x56d811088235F11C8920698a204A5010a788f4b3", "bZx Protocol Token"] !!!NW
#bal = ["0xba100000625a3754423978a60c9317c58a424e3D", "BAL Balancer"] !!!NW

tokens = [bat, dai, amn, ampl, anj, ant, ast, band, bnt]

############################---ARBITRAJE---####################################
# TODO: Would be useful to know transaction fee costs at the time
# I have asked on Discord ...
time_start = time.time()

#amount = 1*10**18  #1 eth
amount = 1*10**17  

for i in tokens:
    #BUY IN V1, SELL IN V2
    take_v1 = uniswap_v1.get_eth_token_input_price(i[0], amount)
    give_v2 = uniswap_v2.get_token_eth_input_price(i[0], take_v1)
    #BUY IN V2, SELL IN V1
    take_v2 = uniswap_v2.get_eth_token_input_price(i[0], amount)
    give_v1 = uniswap_v1.get_token_eth_input_price(i[0], take_v2)
    
    if (give_v2 > amount):
        print("Worth! Spend", web3.fromWei(amount, 'ether'), "ETH in " + i[1] + " in V1, and sell it in V2. Profit =", web3.fromWei(give_v2 - amount, 'ether'), "ETH \n")
    
    if (give_v1 > amount):
        print("Worth! Spend", web3.fromWei(amount, 'ether'), "ETH in " + i[1] + " in V2, and sell it in V1. Profit =", web3.fromWei(give_v1 - amount, 'ether'), "ETH \n")
        
    

time_elapsed = round(time.time() - time_start,2)
print("Program time:", time_elapsed, "seconds")