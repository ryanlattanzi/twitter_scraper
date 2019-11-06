# -----------------------------------------------------------------------------

#                           get_data.py

# Building a Twitter Scraper that grabs tweets

# -----------------------------------------------------------------------------

import ssl
import urllib.request, urllib.parse, urllib.error
import json
import twurl
import os
import time
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class Data:

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
            #print('*********************************')
            #print('     MODE ===> user_timeline')
            #print('*********************************')
            self.user_api_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        elif self.mode == 2:
            print('*********************************')
            print('     MODE ===> home_timeline')
            print('*********************************')
            self.user_api_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        elif self.mode == 3:
            print('*********************************')
            print('     MODE ===> mentions_timeline')
            print('*********************************')
            self.user_api_url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
        self.pull()
        
    #-------------------------------------------------------------------------------------
    #
    #                                 pull(self)
    #
    #    Description: This function will be called in the __init__ function to grab tweets
    #                 and other info to be extracted
    #
    #      Arguments: N/A
    #
    #        Outputs: js: json file: json file with tweets info, exact form can be found by visiting the
    #                                Twitter API page: https://developer.twitter.com/en/docs/tweets/timelines/overview
    #
    #-------------------------------------------------------------------------------------
        
    def pull(self):
        self.checkCount()
        url            = twurl.augment(self.user_api_url, self.params)                
        connection     = urllib.request.urlopen(url, context = ctx)
        data           = connection.read().decode()        
        js             = json.loads(data)
        self.json_file = js
        #print(json.dumps(js, indent=2))
        self.checkTweetCountMatch()
        self.printRemainingCalls(connection)
        
    def checkCount(self):
        self.count = str(self.params['count'])
        if int(self.count) > 200:
            raise Exception('Please enter a count <= 200')
            
    def checkTweetCountMatch(self):
        if len(self.json_file) != int(self.count):
            print('***WARNING*** Only retrieved {} tweet(s), should have retrieved {} tweets.'.format(len(self.json_file), self.count))
            
    def printRemainingCalls(self, connection):
        headers = dict(connection.getheaders())
        print('\n***** Remaining calls: ', headers['x-rate-limit-remaining'], ' *****')
        
    #-------------------------------------------------------------------------------------
    #
    #                                 saveCsv(data_frame, save_loc)
    #
    #    Description: Takes a pandas dataframe and converts it to a CSV.
    #
    #      Arguments: data_frame: pandas df
    #                 save_loc  :       str: string of where to save the CSV. Default value is in
    #                                        'data' folder created in the same directory.
    #
    #        Outputs: N/A
    #
    #-------------------------------------------------------------------------------------
        
    def saveCsv(self, data_frame, save_loc = None):
        filetype      = 'csv'
        self.save_loc = save_loc
        self.checkScreenName()
        self.createSaveLoc(filetype)
        data_frame.to_csv(path_or_buf = self.save_loc, index = False)
        
    #-------------------------------------------------------------------------------------
    #
    #                                 saveJson(json_file, save_loc)
    #
    #    Description: Takes self.json_file and writes it to disk in the save_loc
    #
    #      Arguments: save_loc  :       str: string of where to save the JSON. Default value is in
    #                                        'json' folder created in the same directory.
    #
    #        Outputs: N/A
    #
    #-------------------------------------------------------------------------------------
        
    def saveJson(self, save_loc = None):
        filetype      = 'json'
        self.save_loc = save_loc
        self.checkScreenName()
        self.createSaveLoc(filetype)
        with open(self.save_loc, 'w') as f:
            json.dump(self.json_file, f, indent = 4)
            
    def checkScreenName(self):
        if 'screen_name' not in self.params:
            self.screen_name = input('Please enter the screen name: ')
        else:
            self.screen_name = self.params['screen_name']
            
    def createSaveLoc(self, filetype):
        if not self.save_loc:
            timestr = time.strftime('%Y%m%d_%H%M%S')
            path    = os.path.join('../',filetype)
            if not os.path.exists(path):
                os.mkdir(path)
                self.save_loc = str(path) + '/' + self.screen_name + timestr + '.' + str(filetype)
            else:
                self.save_loc = str(path) + '/' + self.screen_name + timestr + '.' + str(filetype)
        