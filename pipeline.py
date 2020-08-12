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
        #subprocess.run(['python', 'main.py', news_site_uid], cwd='./extract')
        #os.system(f'python ./extract/main.py {news_site_uid}')
        
        ## Move all the .csv file generated with the scraper to the 'tranform' directory
        r = re.compile(r'.*\.(csv|json)')
        extension = re.search(r'(\.csv|\.json)', str(os.listdir(path='./extract'))).group(1)

        try:
            source = list(filter(r.match, os.listdir(path='./extract')))[0]
            #import pdb; pdb.set_trace()

            if source.endswith('.json'):
                shutil.copy(f'./extract/{source}', f'./transform/{news_site_uid}_.json')
            elif source.endswith('.csv'):
                shutil.copy(f'./extract/{source}', f'./transform/{news_site_uid}_.csv')
    
        except:
            logger.warning(f'There is not csv or json file asociated to {news_site_uid}')

def _transform():
    logger.info('Starting transform process')
    
    r = re.compile(r'.*\.(csv|json)')
#    extension = list(filter(r.match, os.listdir(path='./extract')))[0][-3:]
    extension = re.search(r'(\.csv|\.json)', str(os.listdir(path='./extract'))).group(1)[1:]

    import pdb;pdb.set_trace()

    for news_site_uid in news_sites_uids:
        dirty_data_filename = f'{news_site_uid}_.{extension}'
        clean_data_filename = f'clean_{news_site_uid}.{extension}'
        try:
            ## Execute main.py to clean the data and create clean data files
            subprocess.run(['python', 'main.py', f'{news_site_uid}_.{extension}'], cwd='./transform')

            ## Remove the dirty data file
        #    os.remove(f'./transform/{news_site_uid}_.csv')
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
