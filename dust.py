import requests
import datetime

SERVER_ADDR = 'http://14.63.194.241:3000'

GET_DUST_LIST_URL = '/dusts'
INSERT_DUST_URL = '/dusts'


def insert_dust(pm, measured_date=None):
    if pm is None:
        raise AttributeError
    date = measured_date
    if date is None:
        date = datetime.datetime.now()
    payload = {"pm":pm, "measured_date": date}
    response = requests.post(url=SERVER_ADDR+INSERT_DUST_URL, data=payload)
    if response.status_code == 500:
        raise ValueError
    return response
