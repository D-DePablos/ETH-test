# Generate files for use in other scripts
import json

# Save all of the relevant info into TXTs for future reference
if __name__ == "__main__":
    # Token Addresses - Add here
    tokenDic = {
        "ETH": ["0x0000000000000000000000000000000000000000", "ETHEREUM"],
        "BAT": ["0x0D8775F648430679A709E98d2b0Cb6250d2887EF", "BAT"],
        "DAI": ["0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359", "DAI Stablecoin"],
        "AMN": ["0x737F98AC8cA59f2C68aD658E3C3d8C8963E40a4c", "AMN Amon"],
        "AMPL": ["0xD46bA6D942050d489DBd938a2C909A5d5039A161", "AMPL Ampleforth"],
        "ANJ": ["0xcD62b1C403fa761BAadFC74C525ce2B51780b184", "ANJ AragonNetworkJuror"],
        "ANT": ["0x960b236A07cf122663c4303350609A66A7B288C0", "ANT Aragon"],
        "AST": ["0x27054b13b1B798B345b591a4d22e6562d47eA75a", "AST AirSwap"],
        "BAND": ["0xBA11D00c5f74255f56a5E366F4F77f5A186d7f55", "BAND BandToken"],
        "BNT": ["0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C", "BNT Bancor"],
        "BZRX": ["0x56d811088235F11C8920698a204A5010a788f4b3", "bZx Protocol Token"],
        "BAL": ["0xba100000625a3754423978a60c9317c58a424e3D", "BAL Balancer"],
    }

    with open("ArbETH/Utils/Tokens.json", "w") as json_file:
        json.dump(tokenDic, json_file, indent=2, sort_keys=True)
    
    print("Generated Tokens.json!")

    ##########################--SECRETS-#######################################
    # Use secrets file for all of the personal information used for interaction
    # TODO: Use string templates so this does not consist a vulnerability

    API_KEY = input(
        "Please write your INFURA API Key, or enter 'n' to cancel generating new secrets file: "
    )

    if API_KEY != "n":
        assert (
            len(API_KEY) == 32
        ), "Length of API key different to 32. Please check your key"

        # Input wallet name, public and private key
        WALLET_NAME = input(
            "Please write a name for this wallet: "
        )
        
        WALLET_ADDRESS = input(
            "Please write the ETH address (public Key) for the wallet: "
        )

        PRIVATE_KEY = input(
            f"Please write your Private Key for the wallet {WALLET_NAME} : "
        )

        "0x64B976BE4F56dbF10Ca31199eAF63DEc3002b883"
        # Generate dictionary to create valid txt file with secret info
        apiDic = {
            "INFURA_KEY": API_KEY,
            "WALLET_NAME": WALLET_NAME,
            "WALLET_ADDRESS": WALLET_ADDRESS,
            "PRIVATE_KEY": PRIVATE_KEY,
        }

        with open(f"ArbETH/Utils/Secrets.json", "w") as json_file:
            json.dump(apiDic, json_file, indent=2, sort_keys=False)

        print("Successfully created Secrets.json!")
