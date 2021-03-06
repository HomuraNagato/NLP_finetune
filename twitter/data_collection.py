
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

# general imports
import numpy as np
import pandas as pd
import re
import time
import datetime

from textblob import TextBlob
import argparse

# --from_date 2020-03-01 --to_date 2020-03-02 --frequency 4

def initialize():
    
    parser = argparse.ArgumentParser(description='''Collect twitter data pertaining to tweets from known authors and prominent 
                                                    figures to analyze in grover''')
    yesterday = (datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    sixteendays = (datetime.datetime.today()-datetime.timedelta(days=16)).strftime("%Y-%m-%d")
    parser.add_argument('--author', nargs='?', type=str, default='barackobama', help='STR: author or prominent figuary to collect tweets from')
    #parser.add_argument('--keyword', nargs='?', type=str, default='#covid19 OR #coronavirus lang:en', help='STR: hashtag collect tweets based off powertrack rules')
    parser.add_argument('--from_date', nargs='?', type=str, default=sixteendays, help='STR: YYYY-MM-DD inclusive date to start collecting twitter data')
    parser.add_argument('--to_date', nargs='?', type=str, default=yesterday, help='STR: YYYY-MM-DD inclusive date to end collecting twitter data')
    parser.add_argument('--frequency', nargs='?', type=int, default=24, help='number of hours to step by per day. For example frequency = 12, will collect twice: at midnight and noon')
    parser.add_argument('--results_per_call', nargs='?', type=int, default=100, help='number of results per call. Keep at 100 for maximum tweets collected per call')
    parser.add_argument('--max_results', nargs='?', type=int, default=100, help='maxResults is capped at 100 for sandbox account, paid may be 500?')
    parser.add_argument('--data_directory', nargs='?', type=str, default='data', help='directory to store csv data with file name {author,hashtag}_{from_date}_{to_date}.csv')
    
    args = vars(parser.parse_args())
    args['query'] = 'from:'+args['author']
    args['filename'] = args['data_directory'] + '/' +  args['author'] + '_' + args['from_date'] + '_' + args['to_date'] + '.csv'
    #args['query'] = args['keyword']
    #keyword = re.sub('#', '', args['keyword'].split()[0])
    #args['filename'] = args['data_directory'] + '/' +  keyword + '_' + args['from_date'] + '_' + args['to_date'] + '.csv'
    
    return args

def days_to_collect(start, end, frequency):
    '''
    will return an array starting at midnight of desired date to last frequency hour of end date
    start = start date, inclusive
    end = end date, inclusive
    frequency = number of hours to step by per day. For example frequency = 12, will collect twice: at midnight and noon
    '''
    # add one day for right_side border case
    # pd.date_range only allows dates, use rounding dates and closed='right' to get desired dates
    start = datetime.datetime.strptime(start, '%Y-%m-%d') - datetime.timedelta(days=0, hours=int(frequency))
    end = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1, hours=0)
    #print(start, end)
    dates = pd.date_range(start=start, end=end, freq=str(frequency)+'H', closed='left')
    formatted_dates = [ datetime.datetime.strftime(t, '%Y%m%d%H%M') for t in dates ]
    #print(formatted_dates)
    return formatted_dates

def collect_tweets(query, from_date, to_date, results_per_call, max_results, premium_search_args):
    # query: rule to query twitter API. eg if wanting to collect tweets related to bitcoin, then query='bitcoin'
    # maxResults is capped at 100 for sandbox account, even though there should be a next function to get more, it 
    # appears max_results=500 is accepted without any extra work
    # date format: YYYY-mm-DD HH:MM  string format which is automatically called by convert_utc_time. eg '2019-09-09' -> '201909090000'
    # from_date is inclusive. to_date is non-inclusive. Appears to start at from_date and start collecting tweets working
    # backwards to to_date
    collect_rule = gen_rule_payload(pt_rule=query, results_per_call=results_per_call, from_date=from_date, to_date=to_date) 
    print(collect_rule)
    collected_tweets = collect_results(collect_rule, max_results=max_results, result_stream_args=premium_search_args)
    return collected_tweets

def to_df(tweets):
    # create a pandas df from tweets
    S2 = pd.DataFrame(columns=['tweets', 'date', 'user_name', 'user_screen_name', 'user_followers', 
                           'user_friends', 'user_verified', 'user_language', 'retweet_count', 'favorite_count'])

    for i, tweet in enumerate(tweets):
        S2.loc[i] = [tweet['text'], 
                     tweet['created_at'], 
                     tweet['user']['name'], 
                     tweet['user']['screen_name'], 
                     tweet['user']['followers_count'], 
                     tweet['user']['friends_count'], 
                     tweet['user']['verified'], 
                     tweet['user']['lang'], 
                     tweet['retweet_count'], 
                     tweet['favorite_count']] 
    return S2


def activate(args):

    if (datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.strptime(args['from_date'], '%Y-%m-%d')).days < 30:
        print("will use 30-day dev environment")
        premium_search_args = load_credentials("~/.twitter_keys.yaml",
                                          yaml_key="search_tweets_premium_30day",
                                          env_overwrite=False)
    else:
        print("will use full-archive dev environment")
        premium_search_args = load_credentials("~/.twitter_keys.yaml",
                                          yaml_key="search_tweets_premium_fullarchive",
                                          env_overwrite=False)

    print("query: %s" % (args['query']))
    print("start_date: %s end_date: %s" % (args['from_date'], args['to_date']))
    print("frequency: %d max_results: %d" %(args['frequency'], args['max_results']))
    print("file_name from args:", args['filename'])
    
    test_dates = days_to_collect(args['from_date'], args['to_date'], args['frequency'])
    print("test dates\n", test_dates)
                        

    user_input = input("press enter to proceed and any other button to cancel: ")
    
    if user_input != '':
        print("aborting")
        exit(0)
    
    tweets = []
    for i in range(0,len(test_dates[:-1])):
        # test_dates reversed. Eg. 2018-10-31 -> 2018-10-30
        # collect_tweets requires forward collection: collect_tweets(from, to, max_results=100)
        tweets = np.append(tweets, collect_tweets(args['query'], test_dates[i], test_dates[i+1], args['results_per_call'], args['max_results'], premium_search_args))

        # Requests are limited to 30 per minute for sandbox, 60 for subscriptions 
        # Requests are limited to 10 per second
        num_calls = (i + 1) * args['max_results']//args['results_per_call']
        if num_calls % 5 == 0 and num_calls % 20 != 0:
            print("waiting 10 seconds")
            time.sleep(10)

    # flip tweets back so that the rows are in increasing days
    tweets = list(reversed(tweets))

    S2 = to_df(tweets)
    print("collected tweets\n", S2)

    # save file to csv
    S2.to_csv(args['filename'], index=False)
    print('saved file', args['filename'])

if __name__ == '__main__':
    args = initialize()
    activate(args)
