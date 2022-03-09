import logging
import requests as requests
from timeit import default_timer as timer
from dotenv import dotenv_values
from requests.adapters import HTTPAdapter
from retry import retry
from urllib3 import Retry
from modules.FetchAndDecode.configuration import configuration

from modules.FetchAndDecode.Consts import ETHERSCAN_API_KEY, TRANSACTION_DOWNLOADER, MAX_ATTEMPTS, RETRY_STATUS_CODES, \
    RETRY_STRATEGY, MAX_LIMIT_RETRY_STRATEGY, INITIAL_DELAY, BACKOFF

config = configuration[TRANSACTION_DOWNLOADER]
maxLimitRetryStrategyConfig = config[MAX_LIMIT_RETRY_STRATEGY]

"""
This class downloads the data using the api
We use here 2 retries mechanisms:
1. Built-in mechanism of request library
2. We throw exception for throttling, because the api return 200 for this situation. We wrapped it with another
retry mechanism.
"""


def downloadTransactionsByUser(targetUser: str, startBlock: int, endBlock: int, page: int, offset: int) -> requests:
    etherscanApiKey = dotenv_values()[ETHERSCAN_API_KEY]
    http = getHttpSession()

    try:
        endTime, response, startTime = downloadTransactionByUserOperation(endBlock, etherscanApiKey, http, offset, page,
                                                                          startBlock, targetUser)
    except Exception as err:
        logging.error(f"An exception error while downloading transactions for user {targetUser}: {err}")
    else:
        logging.info(f"Transactions download succeed, for user {targetUser}, and took {endTime - startTime} seconds")
    finally:
        http.close()
        return response


@retry(tries=maxLimitRetryStrategyConfig[MAX_ATTEMPTS],
       delay=maxLimitRetryStrategyConfig[INITIAL_DELAY],
       backoff=maxLimitRetryStrategyConfig[BACKOFF])
def downloadTransactionByUserOperation(endBlock, etherscanApiKey, http, offset, page, startBlock, targetUser):
    startTime = timer()
    response = http.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={targetUser}"
                        f"&startblock={startBlock}"
                        f"&endblock={endBlock}"
                        f"&page={page}"
                        f"&offset={offset}"
                        f"&sort=asc&"
                        f"apikey={etherscanApiKey}")
    endTime = timer()
    if response.json()['result'] == "Max rate limit reached":
        raise Exception("Max rate limit reached")
    return endTime, response, startTime


def getHttpSession():
    retryStrategy = getRetryStrategy()
    adapter = HTTPAdapter(max_retries=retryStrategy)
    http = requests.Session()
    http.mount("https://", adapter)
    return http


def getRetryStrategy():
    retryStrategyConfig = config[RETRY_STRATEGY]
    return Retry(
        total=retryStrategyConfig[MAX_ATTEMPTS],
        status_forcelist=retryStrategyConfig[RETRY_STATUS_CODES])
