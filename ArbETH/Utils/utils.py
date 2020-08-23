import json


def getJSONinfo(file):
    """
    Get Information from a txt file within Utils directory
    """
    with open(f"ArbETH/Utils/{file}", "r") as openfile:
        JSONinfo = json.load(openfile)

    return JSONinfo


class Secrets():
    def __init__(self):
        try:
            secrets = getJSONinfo("Secrets.json")
        except FileNotFoundError:
            raise Exception("Secrets.json file not found. Have you run SetupFiles.py?")

        # These properties can be more or less depending on individual needs
        self.infura_key = secrets["INFURA_KEY"]
        self.wallet_name = secrets["WALLET_NAME"]
        self.wallet_address = secrets["WALLET_ADDRESS"]
        self.private_key = secrets["PRIVATE_KEY"]
    
    def __repr__(self):
        return(f"\nSecrets for account name {self.wallet_name} at {self.wallet_address}, \n"\
            f"Connected to Infura at {self.infura_key} \n")

