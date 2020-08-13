# Newspaper ETL Process

This project uses a web scraper to extract data from some news websites. It is based on the procedure ETL (Extract, Transform, and Load).

  
The steps of this script are the following:

1. It extracts the data from the websites using the scraper in the folder 'extract'. All the data is saved first in JSON Files.

2. All the data saved in JSON is processed with Pandas, it is cleaned, modified and complemented, then it is exported in a clean CSV.

3. Once the data is already clean it is stored in an SQLite Database in the 'load' directory.

  

To use the script you have to install all the dependencies from `requirements.txt` and run the file `pipeline.py`

# Extract data from other sources

If you want to extract data from a different newspaper site you can modify the file `./extract/config.yaml`. You have to follow the established format and insert the new data with the link and the CSS Selectors from the newspaper site that you chose. Once you already have done that you can run the scraper, and in case that you want to verify that the data is being properly extracted you can change the variable `_DEBUGGING` that is in `.extract/newspaper_scraper.py`, if you do that you can interact with each of the elements extracted (`title, body, date`).