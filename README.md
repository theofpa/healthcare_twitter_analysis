Coursolve Healthcare Twitter Analysis project
===========================
Try a sample file
=================
Before trying the instructions below, just download one of the sample .csv files and play around. They may have enough data to get you started with basic analyses and visualizations.

I. Setup
========
1. Pull these files onto your computer 
  - twitter_functions.py
  - add_twitter_data_bulk.py   
  - twitter_credentials.py 
  
2. Note: **add_twitter_data_bulk.py** replaces *add_twitter_data.py*  
         you must download the new version of **twitter_functions.py**

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

The program will notify you after every batch; the output file is the name of the input file with "_full" appended. Twitter sometimes returns less data than we requested, in which case we stop and request a new batch. Rows processed up to an id mismatch are retained.

This updated code gets MUCH further before running into Twitter's throttle (I processed over 10,000 lines during testing before I hit it) but it's still there. However, as before, if any input lines have been processed by that point they WILL be written to the output file.

This is version 0.2.   
- Batch processing has been added. 
- POST processing is recommended by Twitter but I don't currently see the need.
- If anyone want me to parse out place names, send me a python list   
  `place_names = ["Boston","Hong Kong", ...]`  
  Don't include junk like DE for Delaware or IN for Indiana


This version is pretty robust, so you ought to really be able to make progress. But bugs undoubtedly remain and if you encounter problems I will try to help: george@georgefisher.com