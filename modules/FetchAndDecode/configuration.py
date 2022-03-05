from modules.FetchAndDecode.Consts import TRANSACTION_DOWNLOADER, RETRY_STRATEGY, MAX_ATTEMPTS, RETRY_STATUS_CODES, \
    TRANSACTION_MAP_DECODER, START_BLOCK, END_BLOCK, PAGE, OFFSET, DOWNLOAD_PARAMS, MAX_LIMIT_RETRY_STRATEGY, \
    INITIAL_DELAY, BACKOFF

configuration = {
    TRANSACTION_DOWNLOADER: {
        RETRY_STRATEGY: {
            MAX_ATTEMPTS: 3,
            RETRY_STATUS_CODES: [429, 500, 502, 503, 504]
        },
        MAX_LIMIT_RETRY_STRATEGY: {
            MAX_ATTEMPTS: 5,
            INITIAL_DELAY: 1,
            BACKOFF: 3
        }
    },
    TRANSACTION_MAP_DECODER: {
        DOWNLOAD_PARAMS: {
            START_BLOCK: 0,
            END_BLOCK: 99999999,
            PAGE: 1,
            OFFSET: 10000 # max results this api endpoint can provide, therefore we get all results in page 1
        }
    }
}
