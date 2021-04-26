# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 20:25:55 2021

@author: Julius Hoffmann
"""


#Import
import csv
import numpy as np
#import time
import datetime
import dateutil.parser as parser




#Constanst
_AGE_GROUPS = {'A00-A04': 0, 'A05-A14': 1, 'A15-A34': 2, 'A35-A59': 3, 'A60-A79': 4, 'A80+': 5, 'unbekannt': 6}
_GENDERS = {'M': 0, 'W': 1, 'unbekannt': 2}
_DATE_TYPES = {'Meldedatum':0 ,'Refdatum':1}
_CASE_TYPES = {'Fall':0 ,'Todesfall':1}



    
def _load_dates():
    """Return a dict with the dates from the start_date to the current date.
    
    Returns
    -------
    dates : dict
        Dictionary containing dates and indexes.
    """
    dates = {}
    end_date = datetime.datetime.now()
    curr_date = parser.isoparse("2020-01-01 00:00:00")
    counter = 0
    while (curr_date <= end_date):
        dates[str(curr_date)] = counter
        curr_date = curr_date + datetime.timedelta(days=1)
        counter += 1  
    return dates
    

def _load_lk_ids():
    """Return a dict with the Landkreise and the indexes.
    
    Returns
    -------
    dates : dict
        Dictionary containing Landkreise and indexes.
    """
    lk_ids = {}
    #lk_names = {}
    csv_file = open("Landkreis_id.csv", mode='r', encoding='UTF-8')
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    next(csv_reader)
    for index,row in enumerate(csv_reader):
        lk_ids[row[0].zfill(5)] = index
        #lk_names[row[0].zfill(5)] = row[1]
    csv_file.close()
    return lk_ids
    



def loadcsv(csv_path:str=''):
    """Load the Covid19 cases from the RKI Cases csv-file and process it.
    
    Parameters
    ----------
    csv_path : str
        path to the RKI Cases csv-file.


    Returns
    -------
    covid_cases : np array.
        returns a numpy array with the loaded covid-19 cases.

    """
    
    #create numpy array with zeros
    lk_ids = _load_lk_ids()
    dates = _load_dates()
    days = len(dates)
    covid_cases = np.zeros((len(lk_ids),days,2,2,7,3),dtype=int)
    data_status = None
    
    #Open RKI_COVID19.csv file and parse through it
    csv_file = open(csv_path, mode='r', encoding='UTF-8')
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    next(csv_reader)
    for index,row in enumerate(csv_reader):
        
        #Prepare indicies
        meldedatum_index = dates[parser.isoparse(row[8].replace("/", "-")).strftime("%Y-%m-%d %H:%M:%S")]
        refdatum_index = dates[parser.isoparse(row[13].replace("/", "-")).strftime("%Y-%m-%d %H:%M:%S")]
        agegroups_index = _AGE_GROUPS[row[4]]
        genders_index = _GENDERS[row[5]]
        lk_index = lk_ids[row[9]]
        
        #update data status
        data_status = row[10].split(',')[0] if data_status == None else data_status
        
        #Fall Meldedatum
        if (int(row[11]) in (0,1)):
            covid_cases  [lk_index]  [meldedatum_index]  [_CASE_TYPES['Fall']]  [_DATE_TYPES['Meldedatum']]  [agegroups_index]  [genders_index] += int(row[6])
        #Todefall Meldedatum
        if (int(row[12]) in (0,1)):
            covid_cases  [lk_index]  [meldedatum_index]  [_CASE_TYPES['Todesfall']]  [_DATE_TYPES['Meldedatum']]  [agegroups_index]  [genders_index] += int(row[7])
        
        #Fall Refdedatum
        if (int(row[11]) in (0,1)):
            covid_cases  [lk_index]  [refdatum_index]  [_CASE_TYPES['Fall']]  [_DATE_TYPES['Refdatum']]  [agegroups_index]  [genders_index] += int(row[6])
        #Todefall Refdedatum 
        if (int(row[12]) in (0,1)):
            covid_cases  [lk_index]  [refdatum_index]  [_CASE_TYPES['Todesfall']]  [_DATE_TYPES['Refdatum']]  [agegroups_index]  [genders_index] += int(row[7])
    

    csv_file.close()
    np.save('covid_cases_numpy',covid_cases)
    
    
    
class Cases:
    def __init__(self,cases, case_description):
        """Construct the object.
        
        Parameters
        ----------
        cases : ndarray
            The numpy array containing the cases for a given day.
        case_description : str
            The description of the case type.
        Returns
        -------
        None.
        """
        self.cases = cases
        self.case_description = case_description
        #self.descriptions = descriptions
        
    def __str__(self):
        """Convert to formal string for print() representation.
        
        Returns
        -------
        ndarray as string : str
            Returns the object's ndarray as a string.

        """
        return str(self.cases)
        
    
    def by_gender(self,frequency='absolute',decimals=3):
        result = self.cases.sum(axis=0)
        result_all = result.sum(axis=0)
        if (frequency.lower() == 'absolute' or result_all == 0):
            return_data = {}
            for index, key in enumerate(_GENDERS.keys()):
                return_data[self.case_description+'_'+key] = result[index]
            return return_data
            #return {'m':result[0],'w':result[1],'unbekannt':result[2]}
        elif (frequency.lower() == 'relative' and result_all != 0):
            return_data = {}
            for index, key in enumerate(_GENDERS.keys()):
                return_data[self.case_description+'_'+key] = round(result[index]/result_all,decimals)
            return return_data 
            #return {'m':round(result[0]/result_all,decimals),'w':round(result[1]/result_all,decimals),'unbekannt':round(result[2]/result_all,decimals)}
        
    def by_age(self,frequency='absolute',decimals=3):
        result = self.cases.sum(axis=1)
        result_all = result.sum(axis=0)
        if (frequency.lower() == 'absolute' or result_all == 0):
            return_data = {}
            for index, key in enumerate(_AGE_GROUPS.keys()):
                return_data[self.case_description+'_'+key] = result[index]
            return return_data
            #return {'A00-A04':result[0],'A05-A14':result[1],'A15-A34':result[2],'A35-A59':result[3],'A60-A79':result[4],'A80+':result[5],'unbekannt':result[6]}
        elif (frequency.lower() == 'relative' and result_all != 0):
            return_data = {}
            for index, key in enumerate(_AGE_GROUPS.keys()):
                return_data[self.case_description+'_'+key] = round(result[index]/result_all,decimals)
            return return_data
            #return {'A00-A04':round(result[0]/result_all,decimals),'A05-A14':round(result[1]/result_all,decimals),'A15-A34':round(result[2]/result_all,decimals),'A35-A59':round(result[3]/result_all,decimals),'A60-A79':round(result[4]/result_all,decimals),'A80+':round(result[5]/result_all,decimals),'unbekannt':round(result[6]/result_all,decimals)}
     
    def by_ageandgender(self,frequency='absolute',decimals=3):
        return_data = {}
        result_all = self.cases.sum(axis=0).sum(axis=0)
        for age_index,age in enumerate(_AGE_GROUPS.keys()):
            for gender_index,gender in enumerate(_GENDERS.keys()):
                if (frequency.lower() == 'absolute' or result_all == 0):
                    return_data[self.case_description+'_'+age+'_'+gender] = self.cases[age_index][gender_index]
                elif (frequency.lower() == 'relative' and result_all != 0):
                    return_data[self.case_description+'_'+age+'_'+gender] = round(self.cases[age_index][gender_index]/result_all,decimals)
        return return_data
    
    def by_cases(self):
        result = {}
        result[self.case_description] = self.cases.sum(axis=0).sum(axis=0)
        return result
    


    
    
def kumFälle(date='2021-01-01 00:00:00', region_id='0', date_type='Meldedatum'):
    """Return the cumulated Covid19 cases for the given day and region.
    
    Parameters
    ----------
    date : str, optional
        The date. The default is '2021-01-01 00:00:00'.
    region_id : str, optional
        Region. The default is '0'.
    date_type : str, optional
        The type of date. The default is 'Meldedatum'.

    Returns
    -------
    Object of class Case : Case object
        Returns an object of the class Case.
    """
    covid_cases = np.load('covid_cases_numpy.npy')
    dates = _load_dates()
    datetype_index = _DATE_TYPES[date_type]
    
    if (int(region_id) == 0):
        result = covid_cases[0:,0:dates[date]+1,0,datetype_index].sum(axis=0).sum(axis=0)

    elif (int(region_id) >= 1 and int(region_id) <= 16):
        lk_ids = _load_lk_ids()
        result = np.zeros((7,3),dtype=int)
        for value,index in list(lk_ids.items()):
            if (value[0:2]==region_id.zfill(2)):
                result = np.add(result,covid_cases[index,0:dates[date]+1,0,datetype_index].sum(axis=0))
        
    elif (int(region_id) > 1000):
        lk_id = _load_lk_ids()[region_id.zfill(5)]
        result = covid_cases[lk_id,0:dates[date]+1,0,datetype_index].sum(axis=0)
        
    return Cases(result, 'kumFälle_{}'.format(date_type))
    
    
def kumTodesfälle(date='2021-01-01 00:00:00', region_id='0', date_type='Meldedatum'):
    """Return the cumulated Covid19 deaths for the given day and region.
    
    Parameters
    ----------
    date : str, optional
        The date. The default is '2021-01-01 00:00:00'.
    region_id : str, optional
        Region. The default is '0'.
    date_type : str, optional
        The type of date. The default is 'Meldedatum'.

    Returns
    -------
    Object of class Case : Case object
        Returns an object of the class Case.
    """
    covid_cases = np.load('covid_cases_numpy.npy')
    dates = _load_dates()
    datetype_index = _DATE_TYPES[date_type]
    
    if (int(region_id) == 0):
        result = covid_cases[0:,0:dates[date]+1,1,datetype_index].sum(axis=0).sum(axis=0)
        
    elif (int(region_id) >= 1 and int(region_id) <= 16):
        lk_ids = _load_lk_ids()
        result = np.zeros((7,3),dtype=int)
        for value,index in list(lk_ids.items()):
            if (value[0:2]==region_id.zfill(2)):
                result = np.add(result,covid_cases[index,0:dates[date]+1,1,datetype_index].sum(axis=0))
        
    elif (int(region_id) > 1000):
        lk_id = _load_lk_ids()[region_id.zfill(5)]
        result = covid_cases[lk_id,0:dates[date]+1,1,datetype_index].sum(axis=0)
        
    return Cases(result, 'kumTodesfälle_{}'.format(date_type))


def neueFälle(date='2021-01-01 00:00:00', region_id='0', date_type='Meldedatum'):
    """Return the new Covid19 cases for the given day and region.
    
    Parameters
    ----------
    date : str, optional
        The date. The default is '2021-01-01 00:00:00'.
    region_id : str, optional
        Region. The default is '0'.
    date_type : str, optional
        The type of date. The default is 'Meldedatum'.

    Returns
    -------
    Object of class Case : Case object
        Returns an object of the class Case.
    """
    covid_cases = np.load('covid_cases_numpy.npy')
    dates = _load_dates()
    datetype_index = _DATE_TYPES[date_type]
    
    if (int(region_id) == 0):
        result = covid_cases[0:,dates[date],0,datetype_index].sum(axis=0)#.sum(axis=0)

    elif (int(region_id) >= 1 and int(region_id) <= 16):
        lk_ids = _load_lk_ids()
        result = np.zeros((7,3),dtype=int)
        for value,index in list(lk_ids.items()):
            if (value[0:2]==region_id.zfill(2)):
                result = np.add(result,covid_cases[index,dates[date],0,datetype_index])
        
    elif (int(region_id) > 1000):
        lk_id = _load_lk_ids()[region_id.zfill(5)]
        result = covid_cases[lk_id,dates[date],0,datetype_index]
        
    return Cases(result, 'neueFälle_{}'.format(date_type)) 

    
def neueTodesfälle(date='2021-01-01 00:00:00', region_id='0', date_type='Meldedatum'):
    """Return the new Covid19 desths for the given day and region.
    
    Parameters
    ----------
    date : str, optional
        The date. The default is '2021-01-01 00:00:00'.
    region_id : str, optional
        Region. The default is '0'.
    date_type : str, optional
        The type of date. The default is 'Meldedatum'.

    Returns
    -------
    Object of class Case : Case object
        Returns an object of the class Case.
    """
    covid_cases = np.load('covid_cases_numpy.npy')
    dates = _load_dates()
    datetype_index = _DATE_TYPES[date_type]
    
    if (int(region_id) == 0):
        result = covid_cases[0:,dates[date],1,datetype_index].sum(axis=0)#.sum(axis=0)

    elif (int(region_id) >= 1 and int(region_id) <= 16):
        lk_ids = _load_lk_ids()
        result = np.zeros((7,3),dtype=int)
        for value,index in list(lk_ids.items()):
            if (value[0:2]==region_id.zfill(2)):
                result = np.add(result,covid_cases[index,dates[date],1,datetype_index])
        
    elif (int(region_id) > 1000):
        lk_id = _load_lk_ids()[region_id.zfill(5)]
        result = covid_cases[lk_id,dates[date],1,datetype_index]
        
    return Cases(result, 'neueTodesfälle_{}'.format(date_type))


def neueFälleZeitraum(date='2021-01-01 00:00:00', region_id='0', date_type='Meldedatum', timespan=1):
    """Return the new Covid19 cases for the given day and region.
    
    Parameters
    ----------
    date : str, optional
        The date. The default is '2021-01-01 00:00:00'.
    region_id : str, optional
        Region. The default is '0'.
    date_type : str, optional
        The type of date. The default is 'Meldedatum'.
    timespan : int
        The number of previous days included in the new cases.
        
    Returns
    -------
    Object of class Case : Case object
        Returns an object of the class Case.
    """
    covid_cases = np.load('covid_cases_numpy.npy')
    dates = _load_dates()
    datetype_index = _DATE_TYPES[date_type]
    
    start_date = parser.isoparse(date)-datetime.timedelta(days=timespan)
    
    if (int(region_id) == 0):
        result = covid_cases[0:,dates[str(start_date)]:dates[date],0,datetype_index].sum(axis=0).sum(axis=0)
        
    elif (int(region_id) >= 1 and int(region_id) <= 16):
        lk_ids = _load_lk_ids()
        result = np.zeros((7,3),dtype=int)
        for value,index in list(lk_ids.items()):
            if (value[0:2]==region_id.zfill(2)):
                result = np.add(result,covid_cases[index,dates[str(start_date)]:dates[date],0,datetype_index].sum(axis=0))
                
    elif (int(region_id) > 1000):
        lk_id = _load_lk_ids()[region_id.zfill(5)]
        result = covid_cases[lk_id,dates[str(start_date)]:dates[date],0,datetype_index].sum(axis=0)
        
    return Cases(result, 'neueFälle_{}Tage_{}'.format(timespan,date_type))


def neueTodesfälleZeitraum(date='2021-01-01 00:00:00', region_id='0', date_type='Meldedatum', timespan=1):
    """Return the new Covid19 cases for the given day and region.
    
    Parameters
    ----------
    date : str, optional
        The date. The default is '2021-01-01 00:00:00'.
    region_id : str, optional
        Region. The default is '0'.
    date_type : str, optional
        The type of date. The default is 'Meldedatum'.
    timespan : int
        The number of previous days included in the new cases.
        
    Returns
    -------
    Object of class Case : Case object
        Returns an object of the class Case.
    """
    covid_cases = np.load('covid_cases_numpy.npy')
    dates = _load_dates()
    datetype_index = _DATE_TYPES[date_type]
    
    start_date = parser.isoparse(date)-datetime.timedelta(days=timespan)
    
    if (int(region_id) == 0):
        result = covid_cases[0:,dates[str(start_date)]:dates[date],1,datetype_index].sum(axis=0).sum(axis=0)
        
    elif (int(region_id) >= 1 and int(region_id) <= 16):
        lk_ids = _load_lk_ids()
        result = np.zeros((7,3),dtype=int)
        for value,index in list(lk_ids.items()):
            if (value[0:2]==region_id.zfill(2)):
                result = np.add(result,covid_cases[index,dates[str(start_date)]:dates[date],1,datetype_index].sum(axis=0))
                
    elif (int(region_id) > 1000):
        lk_id = _load_lk_ids()[region_id.zfill(5)]
        result = covid_cases[lk_id,dates[str(start_date)]:dates[date],1,datetype_index].sum(axis=0)
        
    return Cases(result, 'neueTodesfälle_{}Tage_{}'.format(timespan,date_type))








print(neueFälleZeitraum(date='2021-04-21 00:00:00', region_id='0', date_type='Meldedatum', timespan=7).by_cases())
#loadcsv('RKI_COVID19.csv')
