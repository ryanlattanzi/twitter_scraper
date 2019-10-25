# twitter_scraper
This is a collection of modules that work together to pull data from Twitter.

As I make changes to make the scraper more robust, I will add to the repository, but this is a great first step.

Prequisites
-----------

- Python 3.7

- Various libraries to import

## To get the scraper running:

    1. If you don't have a Twitter account, you must make one.
    
    2. Create an App on the Twitter Developer's site: https://developer.twitter.com/
    
    3. Once you have this done, click on 'Details', and then 'Keys and Tokens'.
    
    4. Copy and pase the Consumer key, Consumer secret, Access Token key, Access Token secret (you may have to first 
    generate access tokens) into `hidden.py`. This is the authorization info that will allow you to access web data 
    through your Twitter account.
    
    5. Open `main.py` and configure the mode (right now only 1 and 2 work, and 1 is the most fun to play with) as 
    well as the parameters (mode 1 needs params1 and mode 2 needs params2).
    
    6. You can also configure the 'info' parameter that contains a list of the information you would like to collect.
    You can find other information to return by looking at `json_example.txt', which is an example of the json format
    returned by Twitter's API.
    
    7. Run the program and look at the pandas dataframe that is returned as the variable 'df'. The same information
    is also included as a dictionary stored in the variable 'info'.
    
    8. Enjoy!
    
Explanation of files
--------
Getting the scraper to run is super easy, but here is a more in depth look at the different modules that makes it possible.

- `hidden.py`: As mentioned above, this file simple stores some authorization keys to be used in the next file.

- `oauth.py` : This is a long file that I found by taking the course 'Using Python to Access Web Data' on Coursera. It is an open source piece, and you can read the liscence at the top of the script. This piece is super complicated, and although I don't know exactly what every function or class does, I know that it takes into account the credentials in `hidden.py` and creates a url that authorizes you as the user to access your Twitter feed.

- `twurl.py` : I also got this from the Coursera course mentioned above. The function 'augment' simply creates the url using the various functions in `oauth.py` and returns the final url we will access.

- `get_data.py`:

  
Contributors
--------------

- Ryan Lattanzi
