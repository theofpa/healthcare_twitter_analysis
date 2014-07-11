Coursolve Healthcare Twitter Analysis project
===========================  

The initial purpose of this repo was to distribute a program that would query Twitter for the tweets in the files provided by the project and to add more data. It has accomplished that and evolved.

Try a sample file
=================
Before trying the instructions below, just download one of the sample .csv files and play around. These files have been filled out with the data available from Twitter and will get you started with analyses and visualizations.  

In the Analyses section, below, are a few examples of using these datasets.  

I. Setup
========
1. Pull these files onto your computer 
  - twitter_functions.py
  - add_twitter_data_bulk.py   
  - twitter_credentials.py 
  
2. Note for early adopters ...  
        - **add_twitter_data_bulk.py** replaces *add_twitter_data.py*  
        - **twitter_functions.py** has been updated  

3. Copy in any .csv files you want to convert from   
   https://drive.google.com/folderview?id=0B2io9_E3COquYWdlWjdzU3ozbzg&usp=sharing

4. Modify "twitter_credentials.py" with your personal Twitter credentials  
``` 
def twitter_credentials():  
    """
    A sample of this file is on the repo. Just download it, fill in your info and
    save it in the same path as the other files.
    
    See https://apps.twitter.com/ to get your own credentials
    """
    api_key = " your credentials "  
    api_secret = " your credentials "  
    access_token_key = " your credentials "  
    access_token_secret = " your credentials "  
    return (api_key,api_secret,access_token_key,access_token_secret)  
```

II. Run
=======

In IPython:
```
cd <to the folder with the programs and files>
%run add_twitter_data_bulk.py "the_name_of_your_file.csv"
```

The program will notify you after every batch; the output file is the name of the input file with "_full" appended. Twitter sometimes returns less data than we requested, in which case we stop when we reach an id mismatch and request a new batch. Rows processed up to an id mismatch are retained.

The change from serial to batch processing gets much further before running into Twitter's throttle (I processed well over 10,000 lines during testing before I hit it) but it's still there. As before, if any input lines have been processed by that point they WILL be written to the output file. The new code also runs to completion considerably faster.

This is version 0.2.   
- Batch processing has been added. 
- POST processing is recommended by Twitter but I don't currently see the need.
- If anyone wants me to parse out place names, send me a python list   
  `place_names = ["Boston","Hong Kong", ...]`  
  Don't include junk like DE for Delaware or IN for Indiana


This version is pretty robust, so you ought to really be able to make progress. But bugs undoubtedly remain and if you encounter problems I will try to help: use the "Issues" tab on the right of the GitHub screen and give me as much documentation as you can so I can reproduce the problem. Thanks.

Utilities
=================

- **hashtag_split.py**  
  input:  a csv file that has been processed by add_twitter_data_bulk.py  
  output: a csv file with one row for every hashtag in a row of the input file  
  use:    %run hashtag_split "Tweets_BleedingDisorders_full.csv"  
- **usermentions_split.py**  
  input:  a csv file that has been processed by add_twitter_data_bulk.py  
  output: a csv file with one row for every *user_mentions* item in a row of the input file  
  use:    %run usermentions_split "Tweets_BleedingDisorders_full.csv"  
- **add_sentiment.py**  
  input:  a csv file that has been processed by add_twitter_data_bulk.py  
  output: a csv file with *sentiment* field added based on AFINN-111.txt  
  use:    %run add_sentiment "Tweets_BleedingDisorders_full.csv"  
  
Analyses
=================  


- **Hashtags_and_Score.pdf**  
  A quick look at hashtag and score distributions    
- **Numerical_EDA.pdf**  
  Statistics on the all the numerical fields available      
- **Score_predicted_by_Numerics.pdf**  
  Do any of the numerics predict score?   
- **TextMining.pdf**  
  Rudimentary text mining.    