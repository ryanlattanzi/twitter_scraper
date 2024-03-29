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
    
    5. Open `main_template.py` and configure the mode (right now only 1 and 2 work, and 1 is the most fun to play with) as 
    well as the parameters (mode 1 needs params1 and mode 2 needs params2).
    
    6. You can also configure the 'info' parameter that contains a list of the information you would like to collect.
    You can find other information to return by looking at `json_format.txt', which is an example of the json format
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

- `get_data.py`: The function 'pull' will actually pull the data from the url and return a JSON formatted python object (either a list or dictionary) to be parsed. It also has the options to save the data as a CSV or JSON. I may change the location of the saving feature to a new class of its own.

- `parse.py`: Using the 'info' that is specified in `main.py`, the function 'json_parse' will go through and find these elements in the JSON file, putting them into a dictionary in which the key, value pair corresponds to the information requested. The function 'to_pd_df' simply converts the dictionary into a Pandas dataframe. The other functions further parse some specific pieces of the data to put them into a neater format. 'parse_created_at' and 'parse_entities' are intended for modes 1 and 2, since mode 3 has a different JSON format that will require different methods. These will be added soon.

- `main_template.py`: This simple function is where all of the supporting functions converge to make it happen in one easy click.

- `twitter_data.py`: You can consider this to be an extension of `main_template` since it grabs tweets from a list of recognizable users. It stores all tweets in a Pandas dataframe, and then writes the file to disk as a CSV for further analysis. This was done because of the limited number of calls we have to Twitter per 24 hours, so we can reuse this CSV over and over to get around calling Twitter.

- `rt_count.py`: My attempt with the data gathered by `twitter_data.py` to predict the number of retweets a tweet will have. It uses NLTK for a little bit of text preprocessing and Keras functional API to work with disparate datatypes (text data and numbered data). The architecture is rather simple, using an LSTM for the text input, and a fully connected neural net for the numerical input. As of now, I have played around and gotten the MAE to reach around 4000, which is not great since this means my model predictions are off by an average of 4000 tweets.

## Future Work:

I obviously need to work on mode 3, and will do so soon.

Perhaps I will also implement some machine learning models. So, I will begin to think of some questions/problems that this data can answer/solve.

Thanks for your time, I hope you enjoyed it!

  
Contributors
--------------

- Ryan Lattanzi
