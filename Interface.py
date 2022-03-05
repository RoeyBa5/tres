import logging
from datetime import datetime

from timeit import default_timer as timer

from modules.GraphGenerator.BFSExecutor import BfsExecutor
from modules.GraphGenerator.MongoConnector import MongoConnector


def run():
    connector = MongoConnector()
    while True:
        print('Hello, choose which operation you want to make:')
        print('1. Run BFS on target user')
        print('2. Clean all collections')
        print('3. Get nodes and edges count')
        print('4. Quit')
        operation = input('Enter your choice (1/2/3/4): ')

        if operation == '1':
            # BFS
            logging.info('Starting BFS operation')
            print('Please wait, it may take a while...')
            startTime = timer()
            BfsExecutor(connector, 10, 3)
            endTime = timer()
            logging.info(f'Finished BFS operation, it took {endTime - startTime} seconds')
        if operation == '2':
            connector.deleteAllCollections()
        if operation == '3':
            nodesCount, edgesCount = connector.getNodesAndEdgesCount()
            print(f'Nodes count = {nodesCount}, edges count = {edgesCount}')
        if operation == '4':
            print('Bye!')
            break

        print('Operation is finished')
        print()


if __name__ == '__main__':
    logging.basicConfig(filename=f'logs/logsOfRun{datetime.now().timestamp()}.log', level=logging.INFO)
    logging.info(f'The app is running, started at {datetime.now()}')
    run()
    logging.info(f'The app has stopped, started at {datetime.now()}')
