import yaml
import os
__config = None


def config_dict():
    """
    This function creates a dictionary with the links and the queries of the web sites
    that are going to be scraped
    """  
    global __config
      
    if not __config:
        #import pdb; pdb.set_trace()
        with open('./extract/config.yaml', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
    return config