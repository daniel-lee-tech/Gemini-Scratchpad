import json


import api


def dump_json_to_file(json_response, file_name):
    with open(file_name, 'w') as trades_file:
        json.dump(json_response, trades_file)



# dump_json_to_file(api.get_all_trades_for_account(), "trades.json")


dump_json_to_file(api.get_all_symbol_details(), "symbol_details.json")


# print(get_500_trades_since_timestamp(millisec))

#
# print(get_account_info())
