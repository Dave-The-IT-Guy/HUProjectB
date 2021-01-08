#Source: https://nik-davis.github.io/posts/2019/steam-data-collection/

import time
import requests
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1)
def get_request(url, parameters=None):
    """Return json-formatted response of a get request using optional parameters.

    Parameters
    ----------
    url : string
    parameters : {'parameter': 'value'}
        parameters to pass as part of get request

    Returns
    -------
    json_data
        json-formatted response (dict-like)
    """
    try:
        response = requests.get(url=url, params=parameters)
    except:
        print('SSL Error:')

        for i in range(5, 0, -1):
            print('\rWaiting... ({})'.format(i), end='')
            time.sleep(1)
        print('\rRetrying.' + ' ' * 10)

        # recusively try again
        return get_request(url, parameters)

    if response:
        return response.json()
    else:
        # response is none usually means too many requests. Wait and try again
        print('No response, waiting 10 seconds...')
        time.sleep(10)
        print('Retrying.')
        return get_request(url, parameters)



url = "https://steamspy.com/api.php"
parameters = {"request": "all"}

# request 'all' from steam spy and parse into dataframe
json_data = get_request(url, parameters=parameters)

steam_spy_all = pd.DataFrame.from_dict(json_data, orient='index')

# generate sorted app_list from steamspy data
#app_list = steam_spy_all[['appid', 'name']].sort_values('appid').reset_index(drop=True)
print(steam_spy_all)

