def twitterreq(url, method, parameters):
    """
    Send twitter URL request
    
    Utility function used by the others in this package
    
    Note: calls a function twitter_credentials() contained in
          a file named twitter_credentials.py which must be provided as follows:

            api_key = " your credentials "  
            api_secret = " your credentials "  
            access_token_key = " your credentials "  
            access_token_secret = " your credentials "  
            return (api_key,api_secret,access_token_key,access_token_secret)
          
     This function is based on a shell provided by
     Bill Howe
     University of Washington
     for the Coursera course Introduction to Data Science
     Spring/Summer 2014
     (which I HIGHLY recommend)
    """
    import oauth2 as oauth
    import urllib2 as urllib

    # this is a private function containing my Twitter credentials
    from twitter_credentials import twitter_credentials
    api_key,api_secret,access_token_key,access_token_secret = twitter_credentials()

    _debug = 0

    oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
    oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

    http_method = "GET"


    http_handler  = urllib.HTTPHandler(debuglevel=_debug)
    https_handler = urllib.HTTPSHandler(debuglevel=_debug)

    '''
    Construct, sign, and open a twitter request
    using the hard-coded credentials above.
    '''
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                 token=oauth_token,
                                                 http_method=http_method,
                                                 http_url=url, 
                                                 parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
      encoded_post_data = req.to_postdata()
    else:
      encoded_post_data = None
      url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def lookup_tweet(tweet_id):
    """
    Ask Twitter for information about a specific tweet by its id
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/statuses/show/%3Aid
    
#Use: 
#import json
#from twitter_functions import lookup_tweet
#
#result = lookup_tweet("473010591544520705")
#for foo in result:
#    tweetdata = json.loads(foo)
#    break
# there must be a better way
#
#print json.dumps(tweetdata, sort_keys = False, indent = 4)
    """
    
    url = "https://api.twitter.com/1.1/statuses/show.json?id=" + tweet_id
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_multiple_tweets(list_of_tweet_ids):
    """
    Ask Twitter for information about 
    a bulk list of tweets by id
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/statuses/lookup
    
    Use: 
import json
from twitter_functions import lookup_multiple_tweets

list_of_tweet_ids = ["473010591544520705","473097867465224192"]
result = lookup_multiple_tweets(list_of_tweet_ids)
for foo in result:
    tweetdata_list = json.loads(foo)
    break
# there must be a better way

for tweetdata in tweetdata_list:
    print json.dumps(tweetdata, sort_keys = False, indent = 4)
    """
    
    csv_of_tweet_ids = ",".join(list_of_tweet_ids)
    url = "https://api.twitter.com/1.1/statuses/lookup.json?id=" + csv_of_tweet_ids
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_user(rsarver):
    """
    Ask Twitter for information about a user name
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/users/show
    
Use: 
import json
from twitter_functions import lookup_user

result = lookup_user("flgprohemo")
for foo in result:
    userdata = json.loads(foo)
    break
# there must be a better way

print json.dumps(userdata, sort_keys = False, indent = 4)


# all may be null; have to check
userdata["location"].encode('utf-8')
userdata["description"].encode('utf-8')
userdata["utc_offset"].encode('utf-8')
userdata["time_zone"].encode('utf-8')
userdata["status"]["lang"].encode('utf-8')
    """
    
    url = "https://api.twitter.com/1.1/users/show.json?screen_name=" + rsarver
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_multiple_users(csv_of_screen_names):
    """
    Ask Twitter for information about up to 100 screen names
    The input argument must be a string of screen names separated by commas
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/users/lookup
    
    Version 0.1 uses GET; Twitter urges POST; I will get to that later
    
Use: 
import json
from twitter_functions import lookup_multiple_users

screen_name_list    = ["grfiv","flgprohemo"]
csv_of_screen_names = ",".join(screen_name_list)

result = lookup_multiple_users(csv_of_screen_names)
for foo in result:
    userdata = json.loads(foo)
    break
# there must be a better way

for user in userdata:
    print "For screen name: " + user["screen_name"]
    print json.dumps(user, sort_keys = False, indent = 4)

    """
    
    url = "https://api.twitter.com/1.1/users/lookup.json?screen_name=" + csv_of_screen_names
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def parse_tweet_json(line, tweetdata):
    """
    Take in a line from the file as a dict
    Add to it the relevant fields from the json returned by Twitter
    """
    line["coordinates"]  = str(tweetdata["coordinates"])
    line["favorited"]    = str(tweetdata["favorited"])
    if tweetdata["entities"] is not None:
         if tweetdata["entities"]["hashtags"] is not None:
             hashtag_string = ""
             for tag in tweetdata["entities"]["hashtags"]:
                 hashtag_string = hashtag_string + tag["text"] + "~"
             hashtag_string = hashtag_string[:-1]
             line["hashtags"] = str(hashtag_string.encode('utf-8'))
         else:
             line["hashtags"] = ""
         if tweetdata["entities"]["user_mentions"] is not None:
             user_mentions_string = ""
             for tag in tweetdata["entities"]["user_mentions"]:
                 user_mentions_string = user_mentions_string + tag["screen_name"] + "~"
             user_mentions_string = user_mentions_string[:-1]
             line["user_mentions"] = str(user_mentions_string)
         else:
             line["user_mentions"] = ""
    line["retweet_count"] = str(tweetdata["retweet_count"])
    line["retweeted"]     = str(tweetdata["retweeted"])
    line["place"]         = str(tweetdata["place"])
    line["geo"]           = str(tweetdata["geo"])
    if tweetdata["user"] is not None:
        line["followers_count"]  = str(tweetdata["user"]["followers_count"])
        line["favourites_count"] = str(tweetdata["user"]["favourites_count"])
        line["listed_count"]     = str(tweetdata["user"]["listed_count"])
        line["location"]         = str(tweetdata["user"]["location"].encode('utf-8'))
        line["utc_offset"]       = str(tweetdata["user"]["utc_offset"])
        line["listed_count"]     = str(tweetdata["user"]["listed_count"])
        line["lang"]             = str(tweetdata["user"]["lang"])
        line["geo_enabled"]      = str(tweetdata["user"]["geo_enabled"])
        line["time_zone"]        = str(tweetdata["user"]["time_zone"])
        line["description"]      = tweetdata["user"]["description"].encode('utf-8')
        
    # why no return? Because Python uses call by reference
    # and our modifications to "line" are actually done to
    # the variable the reference to which was passed in
    #return line
    
def find_WordsHashUsers(input_filename, text_field_name="content", list_or_set="list"):
    """
    Input:  input_filename: the csv file
            text_field_name: the name of the column containing the tweet text
            list_or_set: do you want every instance ("list") or unique entries ("set")?
    
    Output: lists or sets of
            words
            hashtags
            users mentioned
            urls
            
    Usage:  word_list, hash_list, user_list, url_list, num_tweets = \
            find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "list")
    
            word_set, hash_set, user_set, url_set, num_tweets =  \
            find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "set")
    """
    import csv
    
    if list_or_set != "set" and list_or_set != "list":
        print "list_or_set must be 'list' or 'set', not " + list_or_set
        return()
    
    if list_or_set == "list":
        word_list = list()
        hash_list = list()
        user_list = list()
        url_list  = list()
    else:
        word_set = set()
        hash_set = set()
        user_set = set()
        url_set  = set()
    
    with open(input_filename, "rb" ) as infile:
       reader     = csv.DictReader(infile)
       lines      = list(reader) # list of all lines/rows in the input file
       totallines = len(lines)   # number of lines in the input file
       
       # read the input file line-by-line
       # ================================
       for linenum, row in enumerate(lines):
        
           content                    = row[text_field_name]
           words, hashes, users, urls = parse_tweet_text(content)
           
           if list_or_set == "list":
               word_list.extend(words)
               hash_list.extend(hashes)
               user_list.extend(users)
               url_list.extend(urls)
           else:
               word_set.update(words)
               hash_set.update(hashes)
               user_set.update(users)
               url_set.update(urls)
           
    if list_or_set == "list":
        return (word_list, hash_list, user_list, url_list, totallines)
    else:
        return (word_set, hash_set, user_set, url_set, totallines)
        
def parse_tweet_text(tweet_text, AFINN=False):
    """
    Input:  tweet_text: a string with the text of a single tweet
            AFINN:      (optional) True (must have "AFINN-111.txt" in folder)
    
    Output: lists of:
              words
              hashtags
              users mentioned
              urls
              
            (optional) AFINN-111 score 
            
    Usage: from twitter_functions import parse_tweet_text 
    
           words, hashes, users, urls = parse_tweet_text(tweet_text)
           
           words, hashes, users, urls, AFINN_score = parse_tweet_text(tweet_text, AFINN=True)
    """
    import re
    
    content = tweet_text.lower()
           
    urls    = re.findall(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", content, re.IGNORECASE)
    content = re.sub(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", "", content, 0, re.IGNORECASE)
   
    hashes  = re.findall(r"#(\w+)", content)
    content = re.sub(r"#(\w+)", "", content, 0)
   
    users   = re.findall(r"@(\w+)", content)
    content = re.sub(r"@(\w+)", "", content, 0)
    
    # strip out singleton punctuation
    raw_words   = content.split()
    words = list()
    for word in raw_words:
        if word in ['.',':','!',',',';',"-","-","?",'\xe2\x80\xa6',"!"]: continue
        words.append(word)
        
    if AFINN:
        sentiment_words, sentiment_phrases = parse_AFINN("AFINN-111.txt")
        AFINN_score = 0
        # single words
        for word in words:
            if word in sentiment_words:
                AFINN_score += sentiment_words[word.lower()]
        # phrases
        for phrase in sentiment_phrases:
            if phrase in words:
                AFINN_score += sentiment_phrases[phrase]
                
        return (words, hashes, users, urls, AFINN_score)
        
    return (words, hashes, users, urls)
    
def parse_AFINN(afinnfile_name):
    """
    Parse the AFIN-111 sentiment file
    
    Input:  afinnfile_name: the [path/] file name of AFIN-111.txt
    
    Output: dicts of:
              sentiment_words: score
              sentiment_phrases: score
            
    Usage: from twitter_functions import parse_AFINN
           sentiment_words, sentiment_phrases = parse_AFINN("AFINN-111.txt")
    """
    afinnfile = open(afinnfile_name)
    
    sentiment_phrases = {}
    sentiment_words   = {}
    for line in afinnfile:
      key, val  = line.split("\t")        
      if " " in key:
        sentiment_phrases[key.lower()] = int(val)
      else:
        sentiment_words[key.lower()] = int(val)
    return (sentiment_words, sentiment_phrases)