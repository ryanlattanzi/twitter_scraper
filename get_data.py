# -----------------------------------------------------------------------------

#                           get_data.py

# Building a Twitter Scraper that follows the Tweets of Donald Trump

# -----------------------------------------------------------------------------

import ssl
import urllib.request, urllib.parse, urllib.error
import json
import twurl


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class get_data:

    #-------------------------------------------------------------------------------------
    #
    #                                 __init__(self, mode, params)
    #
    #    Description: Automatically calls one of three functions depending on the mode to extract
    #                 user timeline data, home timeline data, or mentions timeline data.
    #
    #                 Mode 1: User Timeline    : https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
    #                 Mode 2: Home Timeline    : https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-home_timeline
    #                 Mode 3: Mentions Timeline: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline
    #
    #      Arguments: mode  : int : 1,2,3 corresponding to the data desired in respective order of the above
    #                               descriptions
    #                 params: dict: dictionary of parameters that depend on the mode (see functions below)
    #
    #        Outputs: 
    #
    #    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
    #
    #
    #-------------------------------------------------------------------------------------
    
    
    def __init__(self, mode, params):
        
        self.mode   = mode
        self.params = params
        
        if self.mode == 1:
            
            print('*********************************')
            print('     MODE ===> user_timeline')
            print('*********************************')
            self.user_api_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
            self.json_file    = self.pull12()
            
            
        elif self.mode == 2:
            
            print('*********************************')
            print('     MODE ===> home_timeline')
            print('*********************************')
            self.user_api_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
            self.json_file    = self.pull12()
            
            
        elif self.mode == 3:
            
            print('*********************************')
            print('     MODE ===> mentions_timeline')
            print('*********************************')
            self.user_api_url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
        
    
    #-------------------------------------------------------------------------------------
    #
    #                                 pull12(self, params)
    # ************************** ONLY WORKS WHEM MODE IS 1 OR 2 **************************
    #
    #    Description: This function will be called in the __init__ function to grab tweets
    #                 and other info to be extracted
    #
    #      Arguments: params: dict: ['screen_name': str,
    #                                'count'      : int]
    #
    #        Outputs: js: json file: json file with tweets info, exact form can be found at url below
    #
    #    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
    #
    #
    #-------------------------------------------------------------------------------------
        
        
    def pull12(self):
        
        #screen_name = params['screen_name']
        count       = str(self.params['count'])

        if int(count) > 200:
            raise Exception('Please enter a count <= 200')
        
        url        = twurl.augment(self.user_api_url, self.params)
        
    
        #######################################################################################

        ## Below is an attempt to get non-truncated tweets, but it says I need authorization ##
#       split_url = str(url).split('&')
        
#       split_url.insert(6, 'tweet_mode=extended')
        
#       a = '&'
#       url = a.join(split_url)
#       print(url)
        
        #######################################################################################
        
        
        connection = urllib.request.urlopen(url, context = ctx)
        data       = connection.read().decode()
        
        js         = json.loads(data)
        #print(json.dumps(js, indent=2))
            
        if len(js) != int(count):
            raise Exception('Only retrieved {} tweet(s), should have retrieved {} tweets.'.format(len(js), count))
        
        
        headers    = dict(connection.getheaders())
        print('\n***** Remaining calls: ', headers['x-rate-limit-remaining'], ' *****')
        
        return js
        
        
            
    
    
    
    
    
    
    
    