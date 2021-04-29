# rki-covid19csv-parser
A small python module to work with the RKI_Covid19.csv files issued by the German RKI (Robert Koch Institut) on a daily basis.

## Installation:
```pip install rki-covid19csv-parser```

## Usage:
Initialize the parser and load data from RKI_Covid19.csv file. Because of the daily increasing file size this process can take a while.
```
import rki_covid19csv_parser
  
covid_cases = rki_covid19csv_parser.covid_cases()
```
Once you have loaded the csv file it's possible to save the processed data to a file on your disk. 
This can significantly speed up the process of loading the data if you run your program multiple times.
```
#save file.
covid_cases.save_toFile('desired/path')

#load file.
covid_cases.load_fromFile('path/to/saved/file')
```

