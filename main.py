from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from datetime import datetime
import os
import subprocess
import logging
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def dir_logging():
    if not os.path.exists('dirlog'):
        os.mkdir(f'dirlog')

def set_logging():
    # Obtengo el dia actual
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f'dirlog/{today}.log'

    # Create an empty log file if not exist
    if not os.path.exists(log_file):
        open(log_file, 'a')
    else:
        pass
    # Configuro el log_file, llamo a basicConfig para que cree el archivo con los loggins posteirores
    logging.basicConfig(filename=log_file,
                        encoding='utf-8',
                        level=logging.INFO,
                        filemode='a',
                        format='%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def asyncio_schedule():
    """schedule tasks"""
    def run_spider():
        dir_logging()
        set_logging()
        # Start
        logging.info('Started crawling {}...'.format(datetime.now()))
        # Run scrapy crawl
        subprocess.run('scrapy crawl laptops', shell=True)
        # subprocess.run('scrapy crawl laptops -O ejemplo.csv', shell=True)
        # End
        logging.info('Finished crawling {}...'.format(datetime.now()))

        # logging.shutdown() # para hacer un logging por ejecucion en vez de uno por dia?

    scheduler = AsyncIOScheduler()
    # Add task to crawl per hour between 7a.m to 7p.m
    scheduler.add_job(func=run_spider, trigger='interval', seconds=10)
    # Start process
    scheduler.start()
    print('Press Ctrl+C to exit')

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    # Running message
    print(' APP IS RUNNING '.center(70,'*'))
    print('Started application {}'.format(datetime.now()))
    # Run process
    asyncio_schedule()