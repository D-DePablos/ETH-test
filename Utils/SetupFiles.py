# Generate files for use in other scripts
import json
from os import getcwd

# Save all of the relevant info into TXTs for future reference
if __name__ == "__main__":
    # Wallet addresses
    walletDic = {
        "Dapper": "0x1F46f6485951cB814C812bA6c80a85b2372C9806",
    }

    with open(f"{getcwd()}/Utils/Wallets.txt", "w") as json_file:
        json.dump(walletDic, json_file)

    # Token Addresses - Add here
    tokenDic = {
        "eth": ["0x0000000000000000000000000000000000000000", "ETHEREUM"],
        "bat": ["0x0D8775F648430679A709E98d2b0Cb6250d2887EF", "BAT"],
        "dai": ["0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359", "DAI Stablecoin"],
        "amn": ["0x737F98AC8cA59f2C68aD658E3C3d8C8963E40a4c", "AMN Amon"],
        "ampl": ["0xD46bA6D942050d489DBd938a2C909A5d5039A161", "AMPL Ampleforth"],
        "anj": ["0xcD62b1C403fa761BAadFC74C525ce2B51780b184", "ANJ AragonNetworkJuror"],
        "ant": ["0x960b236A07cf122663c4303350609A66A7B288C0", "ANT Aragon"],
        "ast": ["0x27054b13b1B798B345b591a4d22e6562d47eA75a", "AST AirSwap"],
        "band": ["0xBA11D00c5f74255f56a5E366F4F77f5A186d7f55", "BAND BandToken"],
        "bnt": ["0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C", "BNT Bancor"],
        "bzrx": ["0x56d811088235F11C8920698a204A5010a788f4b3", "bZx Protocol Token"],
        "bal": ["0xba100000625a3754423978a60c9317c58a424e3D", "BAL Balancer"],
    }

    with open(f"{getcwd()}/Utils/Tokens.txt", "w") as json_file:
        json.dump(tokenDic, json_file)

    # Private Keys, API Keys
    # Use secrets file for all of the personal information used for interaction, or face consequences!
    API_KEY = input(
        "Please write your INFURA API Key, or enter 'n' to cancel generating new secrets file: "
    )
    PRIVATE_KEY = input(
        "Please write your Private Key, or enter 'n' to cancel generating new secrets file: "
    )

    if (API_KEY or PRIVATE_KEY) == "n":
        pass

    else:
        assert (
            len(API_KEY) == 32
        ), "Length of API key different to 32. Please check your key"

        apiDic = {
            "INFURA_KEY": API_KEY,
            "PRIVATE_KEY": PRIVATE_KEY,
        }

        with open(f"{getcwd()}/Utils/Secrets.txt", "w") as json_file:
            json.dump(apiDic, json_file)
