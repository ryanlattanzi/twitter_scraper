# -----------------------------------------------------------------------------

#                           parse.py

# gets a json document and parses it

# -----------------------------------------------------------------------------



import pandas as pd
from datetime import datetime



class Parser():
    
    #-------------------------------------------------------------------------------------
    #
    #                                 __init__(self):
    #
    #    Description: Initializes the 'tweet_info' attribute that will collect requested information
    #                 about the tweets.
    #
    #      Arguments: params: list: list of strings of information to be added to the tweet_info;
    #                               the available info can be found in the twitter developer documentation
    #
    #        Outputs: tweet_info: dict: dictionary where the values are lists
    #
    #-------------------------------------------------------------------------------------
    
    def __init__(self, params):
        
        self.params     = params
        self.tweet_info = {}
        
        for info in params:
            self.tweet_info[info] = []
            
            
    #-------------------------------------------------------------------------------------
    #
    #                           json_parse(self, json_file):
    #
    #    Description: parses the given json file to get the items requested in the __init__ function
    #
    #      Arguments: json_file: format depends on the particular file, usually a list of dictionaries,
    #                            where each dictionary contains info about a tweet
    #                            (this file is usually an object returned by the get_data module)
    #
    #        Outputs: Attribute tweet_info: dict: dictionary where the values are lists
    #
    #-------------------------------------------------------------------------------------
        
    def json_parse(self, json_file):
        
        for tweet in json_file:
            for item in self.params:
                try:
                    temp = tweet[item]
                    self.tweet_info[item].append(temp)
                except:
                    self.tweet_info[item].append('N/A')
                    
    #-------------------------------------------------------------------------------------
    #
    #                           parse_created_at(self):
    #
    #    Description: the 'created_at' parameter in self.params has a lot to unpack. In particular,
    #                 we would like to extract the day of week, year-month-day, time into three columns
    #
    #      Arguments: we will manipulate self.tweet_info
    #                 replace: bool: if True, it will get rid of the 'created_at' key/val because it is redundant
    #
    #        Outputs: N/A (we will manipulate self.tweet_info)
    #
    #-------------------------------------------------------------------------------------
    
    def parse_created_at(self, replace = True):
        
        self.tweet_info['day']       = []
        self.tweet_info['date_time'] = []
        
        created_at = self.tweet_info['created_at']
        
        for creation in created_at:
            
            creation = creation.split()
            day      = creation[0]
            dt       = ' '.join([creation[1], creation[2], creation[-1], creation[3]])
            
            # Converting the ymd and time strings to datetime objects
            dt  = datetime.strptime(dt, '%b %d %Y %H:%M:%S')
            
            self.tweet_info['day'].append(day)
            self.tweet_info['date_time'].append(dt)
            
        if replace:
            del self.tweet_info['created_at']
    
    #-------------------------------------------------------------------------------------
    #
    #                           parse_entities(self):
    #
    #    Description: the 'entities' parameter in self.params has a lot to unpack. In particular,
    #                 we would like to extract hashtags, user_mentions, and urls
    #
    #      Arguments: we will manipulate self.tweet_info
    #                 replace: bool: if True, it will get rid of the 'created_at' key/val because it is redundant
    #
    #        Outputs: N/A (we will manipulate self.tweet_info)
    #
    #-------------------------------------------------------------------------------------
    
    def parse_entities(self, replace = True):
        
        self.tweet_info['hashtags']      = []
        self.tweet_info['user_mentions'] = []
        self.tweet_info['url']           = []
        
        entities = self.tweet_info['entities']
        
        for entity in entities:
            
            hashtags      = entity['hashtags']
            user_mentions = entity['user_mentions']
            try:
                url = entity['urls'][0]['url']
            except:
                url = False
            
            if len(hashtags) == 0:
                self.tweet_info['hashtags'].append(None)
            else:
                text = []
                for tag in hashtags:
                    text.append(tag['text'])
                self.tweet_info['hashtags'].append(text)
                
            if len(user_mentions) == 0:
                self.tweet_info['user_mentions'].append(None)
            else:
                sn = []
                for mention in user_mentions:
                    sn.append(mention['screen_name'])
                self.tweet_info['user_mentions'].append(sn)
                
            if url:
                self.tweet_info['url'].append(url)
            else:
                self.tweet_info['url'].append(None)
                
        if replace:
            del self.tweet_info['entities']
                
    #-------------------------------------------------------------------------------------
    #
    #                           to_pd_df(self):
    #
    #    Description: Extremely simple function that takes the tweet_info dictionary and turns it into
    #                 a pandas dataframe
    #
    #      Arguments: N/A
    #
    #        Outputs: Attribute tweet_info_df: pd dataframe of tweet_info dictionary
    #
    #-------------------------------------------------------------------------------------
    
    def to_pd_df(self):

        self.tweet_info_df = pd.DataFrame(data = self.tweet_info)
            
        
        
        
        

