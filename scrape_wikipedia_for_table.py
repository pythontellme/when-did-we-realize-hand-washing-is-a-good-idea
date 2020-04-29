"""
This module contains classes and functions
for scraping and cleaning tables from specific
websites.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

class scraper:
    """
    Used to create an object containing the
    html in a table on a website

    ...

    Attributes
    ----------
    url : str
        The website url we're scraping

    Methods
    -------
    scrape (class_name, tag)
        Returns the html within a specific class with
        a specific tag on the website
    """

    def __init__(self, url):
        """
        Parameters
        ----------
        url: str
            The website url we're scraping
        """
        self.url = url

    def scrape(self, class_name, tag):
        """
        Returns the html within a specific class with
        a specific tag on the website

        Parameters
        ----------
        
        class_name : str
            The html class of the table we're scraping

        tag : str
            The html tag of the table we're scraping
        """
        # Use requests library to get the html
        # of the given url and assign it to variable
        website_url = requests.get(self.url).text
        # Parse through html and create a tree
        soup = BeautifulSoup(website_url,'lxml')
        # Find a subset of html with table tag in
        # a given class
        my_table = soup.find('table',{'class':class_name})
        # Find html in table within given tag
        table_rows = my_table.findAll(tag)
        return table_rows

def wrangle_list (list):
    """
    Returns a pandas dataframe that has rows and columns
    that reflect the html table we're scraping

    Parameters
    ----------
    list : bs4.element.ResultSet
        A beautiful soup object containing html
    """
    
    # Create a pandas dataframe that will mirror the html table
    df = pd.DataFrame(columns = ['Year', 'Births', 'Deaths', 'Clinic'])
    
    # Create 4 lists to hold html for each column in table
    Year = []
    Births = []
    Deaths = []
    Clinic = []

    # Loop through items in beaufiful soup object w html
    # and add to relevant list - skip first two 'rows' since
    # they are headers in table 
    for i in range(2,8):
            Year.append(list[i].findAll('td')[0].string)
            Births.append(list[i].findAll('td')[1].string)
            Deaths.append(list[i].findAll('td')[2].string)
            # The items appended so far are data for 
            # first clinic
            Clinic.append('First')
            Year.append(list[i].findAll('td')[0].string)
            Births.append(list[i].findAll('td')[5].string)
            Deaths.append(list[i].findAll('td')[6].string)
            # The 3 previous items are data for the
            # second clinic
            Clinic.append('Second')

    # Create columns in dataframe using data in lists
    df['Year'] = Year
    df['Births'] = Births
    df['Deaths'] = Deaths
    df['Clinic'] = Clinic

    return df

def wrangle_list2 (list):
    """
    Returns a pandas dataframe that has rows and columns
    that reflect the html table we're scraping

    Parameters
    ----------
    list : bs4.element.ResultSet
        A beautiful soup object containing html
    """
    # Create a pandas dataframe that will mirror the html table
    df = pd.DataFrame(columns = ['Year', 'Births', 'Deaths'])

    # Create 3 lists to hold html for each column in table
    Year = []
    Births = []
    Deaths = []

    # Loop through items in beaufiful soup object w html
    # and add to relevant list - skip first 'row' since
    # it contains headers in table 
    for i in range(1,len(list)):
            # The 'year' string we need to extract is within a 'span'
            # tag in lines 1-24 
            if (i<=24):
                Year.append(list[i].findAll('span')[0].string)
            # The 'year' string is in within a 'td' tag in 
            # other rows 
            else:
                Year.append(list[i].findAll('td')[1].string)

            Births.append(list[i].findAll('td')[2].string)
            Deaths.append(list[i].findAll('td')[3].string)
                    
    # Create columns in dataframe using data in lists
    df['Year'] = Year
    df['Births'] = Births
    df['Deaths'] = Deaths
    
    return df

def remove_line_breaks (df):
    """
    Loop through each item in dataframe and 
    apply strip function which removes leading and 
    trailing characters

    Parameters
    ----------
    df : pandas dataframe
        The dataframe we're cleaning
    """
    for i in df.columns:
        for j in range(len(df)):
             df.loc[j,i] = df.loc[j,i].strip()

def remove_comma (column):
    """
    Loop through each row item in dataframe column
    and remove the ',' character

    Parameters
    ----------
    column : pandas series
        A specific column of the dataframe we're cleaning
    """
    for x in range(len(column)):
        column[x]  = column[x].replace(',','')
    return column