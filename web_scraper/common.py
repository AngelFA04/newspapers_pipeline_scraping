import yaml

__config = None


def config():
    """
    This function creates a dictionary with the links and the queries of the web sites
    that are going to be scraped
    """    
    if not __config:
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
    return config
