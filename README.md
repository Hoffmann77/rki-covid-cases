# rki-covid19csv-parser
A small python module to work with the RKI_Covid19.csv files issued by the German RKI (Robert Koch Institut) on a daily basis.

## Installation:
```pip install rki-covid19csv-parser```

## Usage:
Initialize the parser and load data from RKI_Covid19.csv file.
```
import rki_covid19csv_parser
  
covid_cases = rki_covid19csv_parser.covid_cases()
covid_cases.load_rki_csv('path/to/your/csv')
```
Because of the daily increasing file size of the RKI_Covid19.csv the process of loadingthe file can take some time.

