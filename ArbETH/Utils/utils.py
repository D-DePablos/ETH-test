import json


def getJSONinfo(file):
    """
    Get Information from a txt file within Utils directory
    """
    with open(f"ArbETH/Utils/{file}", "r") as openfile:
        JSONinfo = json.load(openfile)

    return JSONinfo
