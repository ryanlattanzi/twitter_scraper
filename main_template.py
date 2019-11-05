# -----------------------------------------------------------------------------

#                           main_template.py

# Calls the get_data.py module and returns stuff

# -----------------------------------------------------------------------------


import get_data
import parse




###############################################################################

def run():
    
    # Set the mode and necessary parameters for the mode
    mode  = 1
    params1 = {'screen_name': 'jimmyfallon',
               'count'      : 2,
               'tweet_mode' : 'extended'}
    #params2 = {'count' : 10}
    
    # Gets the data and retrieves a JSON file as an attribute of the instance
    inst = get_data.GetData(mode, params1)
    
    # Establishing the information to be collected and parsing the retrieved JSON file
    info = ['full_text', 'retweet_count', 'created_at', 'entities', 'favorite_count', 'in_reply_to_screen_name', 'retweeted', 'type']
    par  = parse.Parser(info)
    par.json_parse(inst.json_file)
    
    # Further parsing the 'created_at' information into a nicer format
    par.parse_created_at()
    
    # Further parsing the 'entities' information into a nicer format
    par.parse_entities()
    
    # Creating a pandas dataframe from the dictionary of information collected and parsed
    par.to_pd_df()
    
    # Saving the dataframe to disk
    #inst.to_csv(par.tweet_info_df)
    inst.to_csv(par.tweet_info_df, save_loc = '../data/bigdata.csv')
    
    # Saving the JSON file to disk
    inst.to_json()
    
    
    
    return par.tweet_info, par.tweet_info_df
    
###############################################################################



###############################################################################

if __name__ == '__main__':
    
    info, df = run()
    
    