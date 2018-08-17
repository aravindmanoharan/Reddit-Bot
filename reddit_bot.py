#!/usr/bin/env python3

# Import all required packages.

import pandas as pd
import requests
import json
from datetime import datetime
import time

# Enter all the categories for which you need to collect the User information.
categories = ['jokes','personalfinance']
fmt = '%Y-%m-%d %H:%M:%S'

# Looping through all the categories.

for category in categories:
    print('Collecting data from ' + category)
    users = []          # Collecting usernames who have posted in this category.
    scores = []         # Collecting the scores for each of their posts.
    post_url = []       # The URL for each of their posts.
    posted_time = []    # The time of each posts.
    count = 0
    loop = True
    a = []
    url = 'http://www.reddit.com/r/' + category + '/new/.json?limit=100'    # Setting the limit to 100 posts per page (That's the maximum the API allows).
    
    # This script collects posts which are posted 6 hours ago (This is a parameter which can be tuned).
    while(loop == True):
        # Use your respective User-Agent of your browser
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'}
        r = requests.get(url,headers=headers)
        listing = json.loads(r.text)
        after = listing['data']['after']
        data = listing['data']['children']
        for i in data:
            updatedTime = time.strftime(fmt, time.gmtime(i['data']['created']))
            if count == 0:
                startTime = datetime.strptime(updatedTime, fmt)
                count += 1
            else:
                endTime = datetime.strptime(updatedTime, fmt)
                diff = abs(startTime - endTime)
                mins = diff.total_seconds() / 60
                a.append(mins)
                if mins >= 360:
                    loop = False
                    break
            users.append(i['data']['author'])
            scores.append(i['data']['score'])
            post_url.append('www.reddit.com' + i['data']['permalink'])
            posted_time.append(datetime.utcfromtimestamp(int(i['data']['created'])).strftime(fmt))
        
        # Change the URL to next page
        url = 'http://www.reddit.com/r/' + category + '/new/.json?limit=100&after={}'.format(after)
    
    # Converting the results to DataFrame and saving it as csv file
    results = pd.DataFrame([users,scores,post_url,posted_time])
    results = results.transpose()
    results.columns = ['User_Name','User_Score','Post_URL','Posted_Time']
    results.to_csv(category + '.csv', sep=',', index=False)