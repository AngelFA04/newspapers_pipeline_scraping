import argparse
import logging
import hashlib
from numpy import NaN
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('spanish'))


from re import sub

logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse

import pandas as pd

logger = logging.getLogger(__name__)

def main(filename):
    """
    Main function
    """
    
    logger.info('Starting cleaning process')

    df = _read_data(filename)

    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    #Filling missing data
    df = _fill_missing_titles(df)

    #Adding UID to the DataFrame
    df = _generating_uids_for_rows(df)
    
    #Clean body rows
    df = _cleaning_body_rows(df)

    #Tokenize title and body
    df = _tokenize_rows(df, 'title')
    df = _tokenize_rows(df, 'body')
    
    #Clean duplicates entries
    df = _remove_duplicate_entries(df, 'title')
    
    #This removes all the rows with NaN values
    df = _drop_rows_with_missing_values(df)

    return df

def _read_data(filename):
    logger.info(f'Reading file {filename}')
    if filename.endswith('.csv'):
        return pd.read_csv(filename, encoding='utf-8')
    elif filename.endswith('.json'):
        return pd.read_json(filename, encoding='utf-8')


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper UID')
    newspaper_uid = filename.split('_')[0]

    logger.info(f'Newspaper uid detected: {newspaper_uid}')

    return newspaper_uid


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info(f'Filling newspaper_uid column with {newspaper_uid}')
    df['newspaper_uid'] = newspaper_uid

    return df


def _extract_host(df):
    logger.info('Extracting host from url')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

    return df


def _fill_missing_titles(df):
    logger.info('Filling missing titles')
    missing_titles_mask = df['title'].isna()
    missing_titles =  (
        df[missing_titles_mask]['url'].str.extract(
            r'(?P<missing_titles>[^/]+)$'
            ).applymap(lambda title: ' '.join(title.split('-')).replace('.html', '')))

    df.loc[missing_titles_mask, ['title']] = missing_titles.loc[:, 'missing_titles']

    return df


def _generating_uids_for_rows(df):
    logger.info('Generating UIDs for each row')

    uids = (
    df
    .apply(lambda row: hashlib.md5(bytes(row['url'], encoding='utf-8')),axis=1)
    .apply(lambda hash_object: hash_object.hexdigest())
    )
    df['uid'] = uids
    
    return df.set_index(['uid'])


def _cleaning_body_rows(df):

    df['body'] = df.apply(lambda row: sub(r'[\t\n\r]',r'',row['body']) ,  axis=1)
    df['title'] = df.apply(lambda row: sub(r'[\t\n\r]',r'',row['title']) ,  axis=1)

    return df


def tokenize_column(df, column_name):
    return (
        df.dropna()
        .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
        .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
        .apply(lambda tokens: map(str.lower, tokens))
        .apply(lambda word_list: list( filter(lambda word: word not in stop_words, word_list)) )
    )


def _tokenize_rows(df, column_name):
    logger.info('Tokenizing DataFrame rows')
 
    try:
        df[f'{column_name}_tokens'] = tokenize_column(df, column_name)
    except:
        logger.warning(f'There was an error tokenizing the {column_name} column.')    
        df[f'{column_name}_tokens'] = list()
        df[f'n_tokens_{column_name}'] = df[f'{column_name}_tokens'].apply(len)
        return df
    
    df[f'{column_name}_tokens'][(df[f'{column_name}_tokens']).isna()] = ''
    df[f'n_tokens_{column_name}'] = df[f'{column_name}_tokens'].apply(len)

    df[f'{column_name}_tokens'][(df[f'{column_name}_tokens']).isna()] = NaN

    return df


def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicates entries')
    return df.drop_duplicates(subset=column_name, keep='first')


def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with NaN values')
    return df.dropna()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #Introduce the file dataset
    parser.add_argument('filename', help='The path to the dirty data', type=str)
    args = parser.parse_args()

    df = main(args.filename)
    print(df)
    
    #Exporting to a CSV
    filename = f"clean_{sub(r'(.csv|.json)', '', args.filename)}"
    logger.info(f'Saving DataFrame in CSV File in {filename}')
    df.to_csv(f'{filename}.csv', encoding='utf-8', header=True, index_label='uid')