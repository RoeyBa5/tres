import unittest
from modules.GraphGenerator.MongoConnector import MongoConnector


class MongoConnectorTester(unittest.TestCase):
    connector = MongoConnector()

    def testMongoConnector(self):
        self.connector.client.test

    def testUpsertUserNodes(self):
        self.connector.upsertUserNodes([123, 1234])
        result = self.connector.userCollection.find({"$or": [{"userId": 123}, {"userId": 1234}]})

        actualUsers = [result.next()['userId'], result.next()['userId']]
        self.assertIn(123, actualUsers)
        self.assertIn(1234, actualUsers)

    def testUpsertUserNodes(self):
        self.connector.upsertTransactionEdges([
            {'from': 123, 'to': 1234, 'hashes': ['xyz', 'abc']},
            {'from': 1234, 'to': 12345, 'hashes': ['pkh', 'lkj', 'mnb']}
        ])
        result = self.connector.transactionCollection.find({"$or": [{"from": 123}, {"from": 12345}]})

        actualEdges = [result.next()['transactionHashes'], result.next()['transactionHashes']]
        self.assertIn(['xyz', 'abc'], actualEdges)
        self.assertIn(['pkh', 'lkj', 'mnb'], actualEdges)

        # TODO: Add more edge cases, like upserting existing documents and more

        if __name__ == '__main__':
            unittest.main()
