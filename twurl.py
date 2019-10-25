import urllib.request, urllib.parse, urllib.error
import oauth
import hidden






#-------------------------------------------------------------------------------------
#
#                                 augment(url, parameters)
#
#    Description: Takes care of all of the authorization stuff using the 'oauth' library, which is
#                 created by MIT. It takes the tokens and keys from the 'hidden.py' module and creates
#                 a whole URL that we can access the data from.
#
#      Arguments: url       : str : Resource URL that can be found in the twitter documentation
#                 parameters: dict: Depending on the mode, we input the parameters needed to get the
#                                   appropriate URL
#
#        Outputs: oauth_request.to_url(): str: final URL that includes authorizations that we can use
#                                              to access the data
#
#-------------------------------------------------------------------------------------


def augment(url, parameters):
    secrets       = hidden.oauth()
    consumer      = oauth.OAuthConsumer(secrets['consumer_key'], secrets['consumer_secret'])
    token         = oauth.OAuthToken(secrets['token_key'], secrets['token_secret'])
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                    token=token, http_method='GET', http_url=url,
                    parameters=parameters)
    oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(),
                               consumer, token)
    return oauth_request.to_url()
