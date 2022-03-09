import random

from modules.FetchAndDecode.Consts import TRANSACTION_MAP_DECODER, DOWNLOAD_PARAMS, START_BLOCK, END_BLOCK, PAGE, OFFSET
from modules.FetchAndDecode.configuration import configuration
from modules.FetchAndDecode.TransactionsDownloader import downloadTransactionsByUser

config = configuration[TRANSACTION_MAP_DECODER]

"""
This class decodes the result from the api to a map
"""


def getTransactionsMapByUser(targetUser, maxChildren):
    downloadParams = config[DOWNLOAD_PARAMS]
    response = downloadTransactionsByUser(targetUser,
                                          startBlock=downloadParams[START_BLOCK],
                                          endBlock=downloadParams[END_BLOCK],
                                          page=downloadParams[PAGE],
                                          offset=downloadParams[OFFSET])
    if not response:
        dict()

    transactionsMap = getTransactionsMapFromResponse(targetUser, response.json(), maxChildren)

    return transactionsMap


def getTransactionsMapFromResponse(targetUser, responseJson, maxChildren):
    transactionsMap = dict()

    transactionsArray = responseJson['result']

    for transaction in transactionsArray:
        addTransactionToMap(targetUser, transactionsMap, transaction)

    cutTransactionMapForMaxChildren(transactionsMap, maxChildren)

    return transactionsMap


def addTransactionToMap(targetUser, transactionsMap, transaction):
    transactionSource = transaction['from']
    transactionDestination = transaction['to']
    transactionHash = transaction['hash']

    otherUser = transactionDestination if transactionSource == targetUser else transactionSource

    if otherUser in transactionsMap:
        destinationHashList = transactionsMap[otherUser]
        if transactionHash not in destinationHashList:
            destinationHashList.append(transactionHash)
    else:
        transactionsMap[otherUser] = [transactionHash]


def cutTransactionMapForMaxChildren(transactionsMap, maxChildren):
    while len(transactionsMap) > maxChildren:
        transactionsMap.pop(random.choice(list(transactionsMap.keys())))
