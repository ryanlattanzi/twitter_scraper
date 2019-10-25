# twitter_scraper
This is a collection of modules that work together to pull data from Twitter.

As I make changes to make the scraper more robust, I will add to the repository, but this is a great first step.

Prequisites
-----------

- Python 3.7

- Various libraries to import

Explanation of files
--------
For this to work, there is not much you need to do. So, I will first walk you through the necessary steps to get the program working and pulling data from Twitter, and then I will go through a little more in-depth explanations of the various modules.

## To get the files running you must:

    1. If you don't have a Twitter account, you must make one.
    
    2. Create an App on the Twitter Developer's site: https://developer.twitter.com/
    
    3. Once you have this done, click on 'Details', and then 'Keys and Tokens'.
    
    4. Copy and pase the Consumer key, Consumer secret, Access Token key, Access Token secret (you may have to first 
    generate access tokens) into `hidden.py`. This is the authorization step that will allow you to access web data 
    through your Twitter account.
    
    5. Open `main.py` and configure the mode (right now only 1 and 2 work, and 1 is the most fun to play with) as 
    well as the parameters (mode 1 needs params1 and mode 2 needs params2).
    
    6. You can also configure the 'info' parameter that contains a list of the information you would like to collect.
    You can find other information to return by looking at `json_example.txt', which is an example of the json format
    returned by Twitter's API.
    
    7. Run the program and look at the pandas dataframe that is returned as the variable 'df'. The same information
    is also included as a dictionary stored in the variable 'info'.
    
    8. Enjoy!

  
Contributors
--------------

- Ryan Lattanzi
