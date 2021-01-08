#Source: https://nik-davis.github.io/posts/2019/steam-data-collection/

import time
import requests
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
def get_request(url, parameters=None):

    try:
        response = requests.get(url=url, params=parameters)
    except:
        time.sleep(2)
        # recusively try again
        return get_request(url, parameters)

    if response:
        return response.json()
    else:
        # response is none usually means too many requests. Wait and try again
        time.sleep(2)
        return get_request(url, parameters)



url = "https://steamspy.com/api.php"
parameters = {"request": "all"}

# request 'all' from steam spy and parse into dataframe
json_data = get_request(url, parameters=parameters)

steam_spy_all = pd.DataFrame.from_dict(json_data, orient='index')

lst = []

for i in steam_spy_all:
    lst.append(i)

print(lst)