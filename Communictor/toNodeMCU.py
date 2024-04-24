def sendToNodeMCU(data:str):
    """
    writes data on txt file to send to NodeMCU
    """
    f = open("Server/toNodeMCU.txt", "w")
    f.write(data)
    f.close()

def getFromNodeMCU()->str:
    """
    reads data from txt file
    """
    f = open("Server/fromNodeMCU.txt", "r")
    data = f.read()
    f.close()
    return data