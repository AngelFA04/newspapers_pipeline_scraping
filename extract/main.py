from scrapy.crawler import CrawlerProcess
from news_scraper import NewsScraper
import argparse

DEBUGGING = True

def run(newspaper, output):
    """
    Main function of the spider.

    Args:
        newspaper ([str]): [Website name of the newspaper. It has to be in the config.yaml]
        output ([type]): [Filename of the output]
    """
    process = CrawlerProcess(settings={'FEED_URI':f'./extract/{output}.json'})

    process.crawl(NewsScraper, website=newspaper)
    process.start()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('newspaper', help=f'Select a newspaper', type=str)
    parser.add_argument('output', help=f'Select an output', type=str)

    args = parser.parse_args()

    run(args.newspaper, args.output)