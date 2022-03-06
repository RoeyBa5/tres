from dotenv import dotenv_values

MONGO_PASSWORD = 'mongoPassword'
mongoPassword = dotenv_values()[MONGO_PASSWORD]
mongoUrl = f"mongodb://TresRoey:{mongoPassword}@cluster0-shard-00-00.sb5kc.mongodb.net:27017," \
           f"cluster0-shard-00-01.sb5kc.mongodb.net:27017," \
           f"cluster0-shard-00-02.sb5kc.mongodb.net:27017/transactionDb?ssl=true&replicaSet=atlas-djk7lj-shard-0" \
           f"&authSource=admin&retryWrites=true"
TRANSACTION_DB = "transactionDb"
USER_COLLECTION = "userCollection"
TRANSACTION_COLLECTION = "transactionCollection"
TARGET_USER = "0xfb626333099a91ab677bcd5e9c71bc4dbe0238a8"
MAX_MONGO_ATTEMPTS = 3
BFS_EXECUTOR = 'bfsExecutor'
THREADING = 'threading'
TIME_BETWEEN_THREADS = 'timeBetweenThreads'