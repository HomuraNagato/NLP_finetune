
import numpy as np
import pandas as pd
import re
import time
import argparse

def load(congress_num):

    speaker_path = '/mnt/c/Users/Nagato/hacker_data/congress_text/hein-bound/' + congress_num + '_SpeakerMap.txt'
    speech_path = '/mnt/c/Users/Nagato/hacker_data/congress_text/hein-bound/speeches_' + congress_num + '.txt'
    df_speaker = pd.read_csv(speaker_path, sep='|', encoding='latin')
    df_speech = pd.read_csv(speech_path, sep='|', encoding='latin', error_bad_lines=False)

    #print("speaker head\n", df_speaker.head(), "\n", df_speaker.shape)
    #print("speech head\n", df_speech.head(), "\n", df_speech.shape)

    S2 = df_speaker.merge(df_speech, on=['speech_id'], how='inner')

    '''
    # show top four 
    n = 8
    loquacious = S2.groupby('speakerid', as_index=False).agg({"speech": "count"}).sort_values(by='speech', ascending=False).iloc[0:n]
    loquacious.columns = ['speakerid', 'count']

    # join n speakers to filter S2 dataset with all original columns
    S2_t = S2.merge(loquacious, on=['speakerid'], how='inner')
    print("unique contributers\n", S2_t.groupby(['speakerid'], as_index=False).first().sort_values(by='count', ascending=False))
    '''
    #111120961  1110000164     REID        HARRY D 4052
    #111118321  1110000295   DURBIN      RICHARD D 2642
    #111116550  1110002551     AKIN           W. R 1776
    #111120391  1110000276   MCCAIN         JOHN R 1250

    #parties = list(set(S2['party']))
    parties = ['R', 'D']

    filter_speakers = np.empty(0)
    for party in parties:
        S2_f = S2[S2['party'] == party].groupby(['speakerid', 'lastname', 'firstname', 'party'], as_index=False).agg({"speech": "count"}).sort_values(by='speech', ascending=False).iloc[0:2]

        filter_speakers = np.append(S2_f['speakerid'].tolist(), filter_speakers)
        print(S2_f.head())
        
    # show average text length
    S2_f = S2[S2['speakerid'].isin(filter_speakers) ]
    avg_text = S2_f.groupby('speakerid').speech.apply(lambda x: x.str.split().str.len().mean())
    min_text = S2_f.groupby('speakerid').speech.apply(lambda x: x.str.split().str.len().min())
    max_text = S2_f.groupby('speakerid').speech.apply(lambda x: x.str.split().str.len().max())
    print("filtered speech words - min:", min_text, "max:", max_text, "mean:", avg_text)
    
    return S2_f


def cleanse(text):

    # remove all \n with a token for mapping back if desired
    text = re.sub("(\n)", " <|n|> ", text)
    
    # remove whitespace
    text = text.strip().lower()

    # remove procedural words
    procedural_words = [
        'yield', 'motion', 'order', 'ordered', 'quorum', 'roll', 'unanimous',
        'mr\.?', 'mrs\.?', 'speaker\.?', 'chairman\.?', 'president\.?', 'senator\.?',
        'gentleman\.?', 'madam\.?', 'colleague\.?', 
        'today', 'rise', 'pleased to introduce', 'introducing today', 'would like',
        'i suggest the absence of a']

    procedural_words = '|'.join(procedural_words)

    text = re.sub('('+procedural_words+')', "", text)

    # filter sentences that are deemed not long enough
    # actually removed in to_txt func
    if len(text) < 10:
        text = ''

    return text


def to_txt(congress_num, S2):

    filter_path = '/mnt/c/Users/Nagato/hacker_data/congress_text/processed/filtered_speakers_' + congress_num + '.txt'
    
    with open(filter_path, encoding='latin', mode="w+") as f:

        for row in S2.itertuples():

            if len(row.speech.split()) > 10:

                f.write(' <|beginauthor|> ')
                f.write(str(row.speakerid))
                f.write(' <|endofauthor|> ')


                f.write(' <|beginspeech|> ')
                f.write(row.speech)
                f.write(' <|endofspeech|> ')

                f.write(' <|endoftext|> ')

                f.write('\n')


if __name__ == '__main__':

    congress_num = '061'
    S2 = load(congress_num)
    print("S2 head:", S2.head())
    S2['speech'] = [ cleanse(w) for w in S2['speech'] ]
    #to_txt(congress_num, S2)
