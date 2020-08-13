import argparse
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd

from article import Article
from base import Base, engine, Session

logger = logging.getLogger(__name__)

def main(filename):
    Base.metadata.create_all(engine)
    session = Session()
    articles = pd.read_csv(filename, encoding='utf-8')

    for index, row in articles.iterrows():
        logger.info(f'Loading article uid {row["uid"]} into DB')
        article = Article(row['uid'],
                          row['title'],
                          row['body'],
                          row['date'],
                          row['host'],
                          row['newspaper_uid'],
                          row['n_tokens_body'],
                          row['n_tokens_title'],
                          row['body_tokens'],
                          row['title_tokens'],
                          row['url'])

        session.add(article)

    session.commit()
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                          help='The file you want to loadn into the db',
                          type=str)

    args = parser.parse_args()

    main(args.filename)