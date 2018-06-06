import urllib.request
import zipfile
import os
import pandas as pd
import redis
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def download():
    page_url = "https://www.bseindia.com/markets/equity/EQReports/Equitydebcopy.aspx"


    with urllib.request.urlopen(page_url) as response:
        soup = BeautifulSoup(response, 'html.parser')

    link_for_zip = soup.find('a', attrs={'id': 'btnhylZip'}).get('href')

    # now we have the link let's start downloading the file
    f_name = link_for_zip.split("/")[-1]
    with urllib.request.urlopen(link_for_zip) as resp:
        block_size = 10000
        f = open(f_name, 'wb')
        while True:
            buffer = resp.read(block_size)
            if not buffer:
                break
            f.write(buffer)
        f.close()

    # file is downloaded let's extract it
    zipf = zipfile.ZipFile(f_name)
    zipf.extractall("./")
    zipf.close()


    df = pd.read_csv(f_name.split('_')[0] + '.csv')[['SC_CODE', 'SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']]
    r = redis.StrictRedis()

    # calculate the expiration of data
    current_date_time = datetime.now()
    expiration_date_time = current_date_time + timedelta(days=1, hours=-current_date_time.hour, minutes=-current_date_time.minute, seconds=-current_date_time.second)
    expiration_seconds = expiration_date_time.total_seconds()

    # push the results in redis
    for x in df.values[::-1]:
        r.lpush('CODE', x[0])
        r.lpush('NAME', x[1])
        r.lpush('OPEN', x[2])
        r.lpush('HIGH', x[3])
        r.lpush('LOW', x[4])
        r.lpush('CLOSE', x[5])
    r.expire('NAME', expiration_seconds)
    r.expire('CODE', expiration_seconds)
    r.expire('OPEN', expiration_seconds)
    r.expire('CLOSE', expiration_seconds)
    r.expire('HIGH', expiration_seconds)
    r.expire('LOW', expiration_seconds)

    # delete the zip and csv file
    os.remove(f_name)
    os.remove(f_name.split("_")[0] + '.csv')

if __name__ == '__main__':
    download()