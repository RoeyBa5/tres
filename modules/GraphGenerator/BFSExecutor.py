import logging
import queue
import threading
import time
from modules.GraphGenerator.configuration import configuration
from modules.FetchAndDecode.TransactionMapDecoder import getTransactionsMapByUser
from modules.GraphGenerator.Consts import targetUser, BFS_EXECUTOR, TIME_BETWEEN_THREADS, THREADING

config = configuration[BFS_EXECUTOR]


def BfsExecutor(connector, maxChildrenPerNode, maxDepth):
    usersToHandleQueue = getInitialUsersToHandleQueue(targetUser, maxDepth)
    handledUsers = []
    for i in range(maxDepth):
        handleNodesInLevel(connector, handledUsers, i, maxChildrenPerNode, usersToHandleQueue)
        usersToHandleQueue[i].join()


def handleNodesInLevel(connector, handledUsers, i, maxChildrenPerNode, usersToHandleQueue):
    while usersToHandleQueue[i].qsize() > 0:
        try:
            threading.Thread(target=handleUserWorker,
                                    args=(connector, handledUsers, i, maxChildrenPerNode, usersToHandleQueue)).start()
            time.sleep(config[THREADING][TIME_BETWEEN_THREADS])
        except Exception as err:
            logging.error(f"An exception occurred in threading: {err}")


def getInitialUsersToHandleQueue(targetUser, maxDepth):
    usersToHandleQueue = {}
    for i in range(maxDepth + 1):
        usersToHandleQueue[i] = queue.Queue()
    usersToHandleQueue[0].put(targetUser)
    return usersToHandleQueue


def handleUserWorker(connector, handledUsers, i, maxChildrenPerNode, usersToHandleQueue):
    currentUser = usersToHandleQueue[i].get()
    try:
        transactionMap = handleUserTransaction(connector, currentUser, maxChildrenPerNode)
    except Exception as err:
        logging.error(f"An exception occurred while handling user {currentUser}, proceeding without handling it: {err}")
    else:
        handledUsers.append(currentUser)
        addUsersToQueue(transactionMap, usersToHandleQueue, handledUsers, i + 1)
    finally:
        usersToHandleQueue[i].task_done()


def addUsersToQueue(transactionMap, usersToHandle, handledUsers, nextLevel):
    for user in transactionMap.keys():
        if user not in handledUsers:
            usersToHandle[nextLevel].put(user)


def handleUserTransaction(connector, currentUser, maxChildrenPerNode):
    transactionMap = getTransactionsMapByUser(currentUser, maxChildrenPerNode)
    saveDataToMongo(connector, currentUser, transactionMap)
    return transactionMap


def saveDataToMongo(connector, currentUser, transactionMap):
    saveUserNodesToMongo(connector, currentUser, transactionMap)
    saveTransactionEdgesToMongo(connector, currentUser, transactionMap)


def saveUserNodesToMongo(connector, currentUser, transactionMap):
    userNodes = [currentUser]
    for user in transactionMap.keys():
        userNodes.append(user)
    connector.upsertUserNodes(userNodes)


def saveTransactionEdgesToMongo(connector, currentUser, transactionMap):
    transactionsEdges = []
    for transaction in transactionMap.keys():
        transactionsEdges.append({'from': currentUser, 'to': transaction, 'hashes': transactionMap[transaction]})
    connector.upsertTransactionEdges(transactionsEdges)
