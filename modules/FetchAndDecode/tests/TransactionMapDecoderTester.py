import json
import unittest

from modules.FetchAndDecode.TransactionMapDecoder import getTransactionsMapFromResponse


class TransactionMapDecoderTester(unittest.TestCase):
    def setUp(self):
        file = open("testJson.json")
        self.testJson = json.load(file)
        file.close()

    def testJsonToMap(self):
        map = getTransactionsMapFromResponse(self.testJson)

        self.assertEqual(len(map), 2)
        self.assertEqual(len(map['0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a']), 1)
        self.assertEqual(len(map['0x2910543af39aba0cd09dbb2d50200b3e800a63d2']), 4)


if __name__ == '__main__':
    unittest.main()
