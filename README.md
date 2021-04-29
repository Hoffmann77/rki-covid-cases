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
##### Supported methods:
A description of the parameters can be found below. 
| method | description |
| --- | --- |
| ```kumFälle(date, region_id, date_type)``` | cumulated covid19 cases |
| ```kumTodesfälle(date, region_id, date_type)``` | cumulated covid19 deaths |
| ```neueFälle(date, region_id, date_type)``` | new covid19 cases |
| ```neueTodesfälle(date, region_id, date_type)``` | new covid19 cases |

| parameter | input type | description | example |
| --- | :---: | --- | --- |
| date | str | The desired date in the iso format | '2020-06-01 00:00:00' |
| region_id | str | The region id of the desired region. A list can be found further below. | '0' |
| date_type | str | The date type to use.  | 'Meldedatum' |
| timespan | int | The timespan back from the date to be used in the calculation | 3 |

##### Examples:
```
#cumulated covid19 cases for the 01.05.2020 in whole Germany:

covid_cases.kumFälle(date='2020-05-01 00:00:00', region_id=0, date_type='Meldedatum').by_cases()
```


