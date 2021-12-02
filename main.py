import json
import pandas
from datetime import datetime

import api

def create_trades_file_from_json(json_repsonse, file_name="trades.json"):
    with open(file_name, 'w') as trades_file:
        json.dump(json_repsonse, trades_file);


create_trades_file_from_json(api.get_all_trades_for_account())


# print(get_500_trades_since_timestamp(millisec))

#
# print(get_account_info())


