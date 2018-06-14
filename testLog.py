# myapp.py
import logging


import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        print("ran")
        #print(record.__dict__)


def logger1(x):
    print(x)
    print("Y")

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    logger.addhandler(logger)
    x = 1
    logging.info('Finished')

# if __name__ == '__main__':
#     main()



# create logger
logger = logging.getLogger('simple_example')
logger1 = logging.getLogger('sim')
logger.setLevel(logging.DEBUG)
logger1.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger1.addHandler(ch)
h = NullHandler()
logger.addHandler(NullHandler())

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')    


logger1.debug('debug message')