
import numpy as np
import pandas as pd
import re
import argparse

def initialize():
    parser = argparse.ArgumentParser(description='''Collect twitter data pertaining to tweets from known authors and prominent 
                                                    figures to analyze in grover''')

    parser.add_argument('--concat', nargs='+', type=str, help='file to load and inspect data to convert to TFRecord')
    parser.add_argument('--filename', nargs='?', type=str, help='resulting filename of concatted files')

    args = vars(parser.parse_args())
    
    return args
    
if __name__ == '__main__':


    #S2 = pd.read_csv(args['load_data'], encoding='latin')
    args = initialize()

    S2 = pd.DataFrame()

    for path in args['concat']:
        print(path)
        S1 = pd.read_csv(path, encoding='latin')

        S2 = pd.concat([S2, S1], ignore_index=True)

    print(S2.head())
    print(S2.tail())

    S2.to_csv(args['filename'], index=False)
    
