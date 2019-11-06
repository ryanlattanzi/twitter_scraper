# -----------------------------------------------------------------------------

#                           parse.py

# gets a json document and parses it

# -----------------------------------------------------------------------------



import pandas as pd
from datetime import datetime
import objectpath
import numpy as np



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
        for info in self.params:
            self.tweet_info[info] = []
            
    #-------------------------------------------------------------------------------------
    #
    #                           jsonParse(self, json_file):
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
        
    def parseJson(self, json_file):
        for tweet in json_file:
            for item in self.params:   
                if item == 'retweeted':
                    self.checkRetweeted(tweet, item)
                elif item == 'type':
                    self.checkType(tweet, item)
                else:
                    self.extractAllOthers(tweet, item)
                        
    def checkRetweeted(self, tweet, item):
        if 'retweeted_status' in tweet:
            self.tweet_info[item].append(1)
        else:
            self.tweet_info[item].append(0)
    
    def checkType(self, tweet, item):
        tree_obj = objectpath.Tree(tweet)
        try:
            self.tweet_info[item].append(list(tree_obj.execute('$..type'))[-1])
        except:
            self.tweet_info[item].append('text')
                
    def extractAllOthers(self, tweet, item):
        try:
            temp = tweet[item]
            self.tweet_info[item].append(temp)
        except:
            self.tweet_info[item].append(None)
        
    #-------------------------------------------------------------------------------------
    #
    #                           parseCreatedAt(self):
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
    
    def parseCreatedAt(self, replace = True):
        self.tweet_info['day']       = []
        self.tweet_info['date_time'] = []
        created_at = self.tweet_info['created_at']
        for creation in created_at:
            creation = creation.split()
            day, dt  = self.getDayAndDateTime(creation)
            self.tweet_info['day'].append(day)
            self.tweet_info['date_time'].append(dt)
        if replace:
            del self.tweet_info['created_at']
            
    def getDayAndDateTime(self, creation):
        day      = creation[0]
        dt       = ' '.join([creation[1], creation[2], creation[-1], creation[3]])
        dt       = datetime.strptime(dt, '%b %d %Y %H:%M:%S')
        return day, dt
        
    #-------------------------------------------------------------------------------------
    #
    #                           parseEntities(self):
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
    
    def parseEntities(self, replace = True):
        self.tweet_info['hashtags']      = []
        self.tweet_info['user_mentions'] = []
        self.tweet_info['url']           = []
        entities = self.tweet_info['entities']
        for entity in entities:
            hashtags      = entity['hashtags']
            user_mentions = entity['user_mentions']
            self.getHashtags(hashtags)
            self.getUserMentions(user_mentions)
            self.getUrl(entity)
        if replace:
            del self.tweet_info['entities']
            
    def getHashtags(self, hashtags):
        if len(hashtags) == 0:
            self.tweet_info['hashtags'].append(None)
        else:
            text = []
            for tag in hashtags:
                text.append(tag['text'])
            self.tweet_info['hashtags'].append(len(text))
        
    def getUserMentions(self, user_mentions):
        if len(user_mentions) == 0:
            self.tweet_info['user_mentions'].append(None)
        else:
            sn = []
            for mention in user_mentions:
                sn.append(mention['screen_name'])
            self.tweet_info['user_mentions'].append(len(sn))
            
    def getUrl(self, entity):
        try:
            url                    = entity['urls'][0]['url']
            self.tweet_info['url'] = np.append(self.tweet_info['url'], 1)
        except:
            self.tweet_info['url'] = np.append(self.tweet_info['url'], 0)
        
    #-------------------------------------------------------------------------------------
    #
    #                           toPandasDf(self):
    #
    #    Description: Extremely simple function that takes the tweet_info dictionary and turns it into
    #                 a pandas dataframe
    #
    #      Arguments: N/A
    #
    #        Outputs: Attribute tweet_info_df: pd dataframe of tweet_info dictionary
    #
    #-------------------------------------------------------------------------------------
    
    def toPandasDf(self):
        self.tweet_info_df = pd.DataFrame(data = self.tweet_info)
