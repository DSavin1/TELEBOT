import requests
import configparser
import logging

config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(format='%(pathname)s  %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
PATH = 'https://api.telegram.org/bot'

def get_token():
    token = config['DEFAULT']['token']
    return token


if __name__ == '__main__':
    logging.info('Starting')
    token = get_token()



