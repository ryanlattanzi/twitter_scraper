# -----------------------------------------------------------------------------

#                           main.py

# Calls the get_data.py module and returns stuff

# -----------------------------------------------------------------------------


import get_data
import parse




###############################################################################

def run():
    
    # Set the module and necessary parameters for the module
    module  = 1
    params1 = {'screen_name': 'sixers',
               'count'      : 10}
    params2 = {'count' : 10}
    
    # Gets the data and retrieves a json file as an attribute of the instance
    inst = get_data.get_data(module, params2)
    
    info = ['text', 'retweet_count', 'created_at', 'entities', 'favorite_count']
    par  = parse.Parser(info)
    par.json_parse(inst.json_file)
    par.parse_created_at()
    par.parse_entities()
    par.to_pd_df()
    
    return par.tweet_info, par.tweet_info_df
    
###############################################################################



###############################################################################

if __name__ == '__main__':
    
    info, df = run()
    
    
