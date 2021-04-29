# rki-covid19csv-parser
A small python module to work with the RKI_Covid19.csv files issued by the German RKI (Robert Koch Institut) on a daily basis.

## Installation:
```pip install rki-covid19csv-parser```

## Usage:
#### First steps:
Initialize the parser and load data from the RKI_Covid19.csv file.   Because of the daily increasing file size this process can take a while.
```
import rki_covid19csv_parser
  
covid_cases = rki_covid19csv_parser.covid_cases()
```
#### Speeding up the loading process:
Once you have loaded the csv file it's possible to save the processed data to a file on your disk.
This can significantly speed up the process of loading the data if you whish to run your script more than once.
```
#save file.
covid_cases.save_toFile('desired/path')

#load file.
covid_cases.load_fromFile('path/to/saved/file')
```
#### Get the covid19 data:
Until now the following methods are supported:

| method | description |
| --- | --- |
| ```kumFälle(date, region_id, date_type)``` | cumulated covid19 cases |
| ```kumTodesfälle(date, region_id, date_type)``` | cumulated covid19 deaths |
| ```neueFälle(date, region_id, date_type)``` | new covid19 cases |
| ```neueTodesfälle(date, region_id, date_type)``` | new covid19 cases |
