import logging
import pymongo
from timeit import default_timer as timer
from pymongo import UpdateOne, DeleteMany
from retry import retry

from modules.GraphGenerator.Consts import mongoUrl, TRANSACTION_DB, USER_COLLECTION, TRANSACTION_COLLECTION, \
    MAX_MONGO_ATTEMPTS

"""
mongoConnector Object
Includes retries mechanism and bulk writes for efficiency
"""


class MongoConnector:
    def __init__(self):
        self.client = pymongo.MongoClient(mongoUrl)
        self.transactionDb = self.client[TRANSACTION_DB]
        self.userCollection = self.transactionDb[USER_COLLECTION]
        self.transactionCollection = self.transactionDb[TRANSACTION_COLLECTION]

    def upsertUserNodes(self, userNodes):
        bulk = []
        for userNode in userNodes:
            self.__checkIfNodeAlreadyExists(userNodes, userNode)
            bulk.append(UpdateOne({'userId': userNode}, {'$set': {'userId': userNode}}, upsert=True))
        self.__flushChanges(collection=self.userCollection, bulk=bulk, operationType="upsertUserNodes")

    """
    This function is according to Eilon's last reqeust 
    """
    def __checkIfNodeAlreadyExists(self, userNodes, userNode):
        if userNode == userNodes[0]:
            return
        try:
            if self.userCollection.find_one({'userId': userNode}) is not None:
                logging.info(f"About to add an edge that already exists in the graph. The father of the edge is:"
                             f" {userNodes[0]}, the edge is: {userNode}")
        except Exception as err:
            logging.error(f"An error occured while quering DB:{err}")

    def upsertTransactionEdges(self, transactions):
        bulk = []
        for transaction in transactions:
            # To make each edge undirected, we add 2 directed edges
            bulk.append(UpdateOne({'from': transaction['from'], 'to': transaction['to']},
                                  {'$addToSet': {'transactionHashes': {'$each': transaction['hashes']}}},
                                  upsert=True))
            bulk.append(UpdateOne({'from': transaction['to'], 'to': transaction['from']},
                                  {'$addToSet': {'transactionHashes': {'$each': transaction['hashes']}}},
                                  upsert=True))
        self.__flushChanges(collection=self.transactionCollection, bulk=bulk, operationType="upsertTransactionEdges")

    def deleteAllCollections(self):
        bulk = [DeleteMany({})]
        self.__flushChanges(collection=self.userCollection, bulk=bulk, operationType="deleteUserCollection")
        self.__flushChanges(collection=self.transactionCollection, bulk=bulk,
                            operationType="deleteTransactionCollection")

    def getNodesAndEdgesCount(self):
        try:
            edgesCount, nodesCount = self.__getNodesAndEdgesCountWithRetries()
        except Exception as err:
            logging.error(f"An exception error while getting nodes and edges count: {err}")
        else:
            logging.info(f"Get nodes and edges count succeed")
        return nodesCount, edgesCount

    @retry(tries=MAX_MONGO_ATTEMPTS)
    def __getNodesAndEdgesCountWithRetries(self):
        nodesCount = self.userCollection.count_documents({})
        edgesCount = self.transactionCollection.count_documents({})
        return edgesCount, nodesCount

    def getAllEdges(self):
        try:
            edges = self.__getAllEdgesWithRetries()
        except Exception as err:
            logging.error(f"An exception error while getting all edges: {err}")
        else:
            logging.info(f"Get all edges succeed")
        return edges

    @retry(tries=MAX_MONGO_ATTEMPTS)
    def __getAllEdgesWithRetries(self):
        return self.transactionCollection.find()

    def __flushChanges(self, collection, bulk, operationType):
        try:
            startTime = timer()
            self.__bulkWriteWithRetries(collection, bulk)
            endTime = timer()
        except Exception as err:
            logging.error(f"An exception error while operationType={operationType}: {err}")
        else:
            logging.info(f"{operationType} user nodes succeed, it took {endTime - startTime} seconds")

    @retry(tries=MAX_MONGO_ATTEMPTS)
    def __bulkWriteWithRetries(self, collection, bulk):
        collection.bulk_write(bulk)
