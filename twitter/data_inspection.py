
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

# general imports
import numpy as np
import pandas as pd
import re
import time
import datetime

from textblob import TextBlob
import argparse

# plotting and visualization
#import matplotlib
#import matplotlib.pyplot as plt
#%matplotlib inline

def initialize():
    parser = argparse.ArgumentParser(description='''Collect twitter data pertaining to tweets from known authors and prominent 
                                                    figures to analyze in grover''')

    parser.add_argument('--load_data', nargs='?', type=str, default='nytimes_data/nytimes_2020-02-11_2020-02-24.csv', help='file to load and inspect data to convert to TFRecord')

    args = vars(parser.parse_args())
    
    return args
    
    
def load(args):

    print("loading data from %s" % (args['load_data']))
    S2 = pd.read_csv(args['load_data'], encoding='latin')
    return S2

def convert(args, original):

    S2 = pd.DataFrame()
    
    S2['title'] = original['user_name'] + ' ' + original['date']
    #S2['title'] = original['tweets']
    S2['text'] = original['tweets']
    S2['summary'] = np.NaN
    S2['authors'] = original['user_name']
    #print("publish_date", original['date'], "formatted date", original['date'])
    #S2['publish_date'] = pd.to_datetime(original['date'])
    S2['publish_date'] = pd.to_datetime(original['date']).apply(lambda x: datetime.datetime.strftime(x, '%m-%d-%Y'))
    S2['status'] = 'success'
    S2['url'] = 'twitter'
    S2['domain'] = 'twitter'
    S2['warc_date'] = datetime.datetime.today().strftime('%m-%d-%Y')
    S2['split'] = 'train'

    print("formatted twitter data frame \n", S2.columns)

    S2 = S2[S2['text'].str.split().apply(len) > 5 ]

    S2_min = S2['text'].str.split().apply(len).min()
    S2_mean = S2['text'].str.split().apply(len).mean()
    S2_max = S2['text'].str.split().apply(len).max()
    print("text min: %d\t max: %d\t mean: %d\t S2 shape: (%d,%d)" % (S2_min, S2_max, S2_mean, S2.shape[0], S2.shape[1]))

    return S2

def cleanse(text):

    # substitute html
    text = re.sub("(http.*)( |$)", "<|url|>", text)
    
    # substitute @{person}
    # match start with @ symbol, then any character that isn't a space
    # and terminate at a space
    # thus matches '@sensanders', '@sensanders:', etc
    text = re.sub("(@[^\s]+)(\s|$)", "<|user|> ", text)

    # substitute #{hashtag}
    text = re.sub("(#[^\s]+)\s", "<|hashtag|> ", text)

    # https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space
    # remove all other nn-aschii symbols
    text = re.sub("[^\x00-\x7F]+", "", text)

    # remove all \n with a token for mapping back if desired
    text = re.sub("(\n)", " <|n|> ", text)
    
    # remove whitespace
    text = text.strip().lower()

    return text


def to_txt(args, S2):
    with open(re.sub('.csv', '_singleline.txt', args['load_data']), encoding='latin', mode="w+") as f:

        for row in S2.itertuples():
            
            f.write(' <|begindomain|> ')
            f.write(row.domain)
            f.write(' <|endofdomain|> ')
            
            f.write(' <|begindate|> ')
            f.write(row.publish_date)
            f.write(' <|endofdate|> ')

            f.write(' <|beginauthors|> ')
            f.write(row.authors)
            f.write(' <|endofauthors|> ')
            
            f.write(' <|begintitle|> ')
            f.write(row.title)
            f.write(' <|endoftitle|> ')

            f.write(' <|beginarticle|> ')
            f.write(row.text)
            f.write(' <|endofarticle|> ')
            
            f.write(' <|endoftext|> ')
            
            f.write('\n')

            
if __name__ == '__main__':
    args = initialize()
    S2 = load(args)
    #[ Print(i, x) for i, x in enumerate(S2['tweets']) ]
    S2 = convert(args, S2)
    S2['text'] = [ cleanse(w) for w in S2['text'] ]
    #[ print(x) for x in S2['text'][70:90] ]
    to_txt(args, S2)
