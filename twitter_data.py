# -----------------------------------------------------------------------------

#                           twitter_data.py

#  This function takes in a list of users to pull tweets from, and appends all
#  of the information nicely into a big dataframe.

# -----------------------------------------------------------------------------

import pandas as pd
import sys
sys.path.insert(1, '../source')
import get_data
import parse


###############################################################################

def run():
    
    # A list of users for which we would like to collect tweets
    users      = ['jimmyfallon'  , 'shakira'    , 'cnnbrk'       , 'britneyspears'  , 'BillGates',
                  'Twitter'      , 'selenagomez', 'KimKardashian', 'realDonaldTrump', 'MileyCyrus',
                  'ArianaGrande' , 'YouTube'    , 'TheEllenShow' , 'ladygaga'       , 'Cristiano',
                  'taylorswift13', 'rihanna'    , 'justinbieber' , 'katyperry'      , 'BarackObama',
                  'nytimes'      , 'JLo'        , 'KingJames'    , 'CNN'            , 'BrunoMars',
                  'Oprah'        , 'Drake'      , 'SportsCenter' , 'KevinHart4real' , 'wizKhalifa',
                  'LilTunechi'   , 'espn'       , 'NASA'         , 'Harry_Styles'   , 'Louis_Tomlinson',
                  'Pink'         , 'chrisbrown' , 'kanyewest'    , 'EmmaWatson'     , 'elonmusk']
    
    info       = ['full_text', 'retweet_count', 'created_at', 'entities', 'favorite_count', 'in_reply_to_screen_name', 'retweeted', 'type']
    mode       = 1
    count      = 200
    total_data = pd.DataFrame()
    
    for user in users:
    
        # Set the mode and necessary parameters for the mode
        params1 = {'screen_name': user,
                   'count'      : count,
                   'tweet_mode' : 'extended'}
        
        # Runs what 'main_template.py' runs for each user, and appends data to the dataframe 'total_data'
        inst = get_data.GetData(mode, params1)
        
        par  = parse.Parser(info)
        par.json_parse(inst.json_file)
        par.parse_created_at()
        par.parse_entities()
        par.to_pd_df()
        
        total_data = total_data.append(par.tweet_info_df, ignore_index = True)
        
        print('Done with user: ', user)
    
    # Saving the CSV to disk
    inst.to_csv(total_data, save_loc = '../data/big_data.csv')
    
    return total_data
    
###############################################################################



###############################################################################

if __name__ == '__main__':
    
    data = run()








