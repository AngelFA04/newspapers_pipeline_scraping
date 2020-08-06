# Newspaper ETL Process

This project use a web scraper to extract data from some news websites. It is based in the procedure ETL (Extract, Transform and Load).

  

The steps of this script are the following:

1. It extract the data from the websites using the scraper in the folder 'extract'. All the data is saved in CSV Files.

2. All the data saved in CSV is processed with Pandas, it is cleaned, modified and complemented.

3. Once the data is already clean it is stored in a SQLite Database in the 'load' directory.

  

In order to use the script you have to install all the dependences from `requirements.txt` and run the file `pipeline.py`

# Extract data from other sources

If you want to extract data from a diferent newspaper site you can modify the file `config.yaml`. You have to follow the stablished format and insert the new data with the link and the CSS Selectors from the newspaper site that you chose.
