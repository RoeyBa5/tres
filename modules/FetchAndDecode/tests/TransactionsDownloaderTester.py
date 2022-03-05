import unittest

from modules.FetchAndDecode.TransactionsDownloader import downloadTransactionsByUser


class TransactionsDownloaderTester(unittest.TestCase):
    def setUp(self):
        self.testUser = '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a'

    def testDownloader(self):
        response = downloadTransactionsByUser(targetUser=self.testUser, startBlock=0, endBlock=99999, page=1, offset=2)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    # TODO: test retry flow with mock
    # TODO: test exception flow with mock


if __name__ == '__main__':
    unittest.main()
