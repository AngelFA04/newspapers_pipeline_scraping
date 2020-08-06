import logging
logging.basicConfig(level=logging.INFO)
import subprocess
import os
import shutil
import re


logger = logging.getLogger(__name__)
#news_sites_uids = ['eluniversal', 'animalpolitico', 'elpais']
news_sites_uids = ['elpais']


def main():
    _extract()
    _transform()
    _load()
    

def _extract():
    logger.info('Starting extract process')
    for news_site_uid in news_sites_uids:
        ## Execute the extractions of all the news sites
        subprocess.run(['python', 'main.py', news_site_uid], cwd='./extract')
        #os.system(f'python ./extract/main.py {news_site_uid}')
        
        ## Move all the .csv file generated with the scraper to the 'tranform' directory
        r = re.compile(r'.*\.csv')
        try:
            source = list(filter(r.match, os.listdir(path='./extract')))[0]
            shutil.move(f'./extract/{source}', f'./transform/{news_site_uid}_.csv')
        except:
            logger.warning(f'There is not csv file asociated to {news_site_uid}')

def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = f'{news_site_uid}_.csv'
        clean_data_filename = f'clean_{news_site_uid}.csv'
        try:
            ## Execute main.py to clean the data and create clean data files
            subprocess.run(['python', 'main.py', f'{news_site_uid}_.csv'], cwd='./transform')

            ## Remove the dirty data file
            os.remove(f'./transform/{news_site_uid}_.csv')
            ## Move the clean data file into 'load' directory with the '{news_site_uid}.csv' name
            shutil.move(f'./transform/clean_{news_site_uid}_.csv', f'./load/{news_site_uid}_.csv')
        except:
            logger.warning(f'There is not csv file asociated to {news_site_uid} in the "transform" directory')



def _load():
    logger.info('Starting load process')
    for news_site_uid in news_sites_uids:
        clean_data_filename = f'{news_site_uid}.csv'
        try:
            ## Execute the script 'main.py' to load the date into a SQLite Database
            subprocess.run(['python', 'main.py', f'{news_site_uid}_.csv'], cwd='./load')
            pass
            ## Remove the csv file
            os.remove(f'./load/{news_site_uid}_.csv')
        except:
            logger.warning(f'There is not csv file asociated to {news_site_uid} in the "load" directory')




if __name__ == "__main__":
    main()
