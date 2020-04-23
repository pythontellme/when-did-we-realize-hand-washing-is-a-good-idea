import pandas as pd
import requests
from bs4 import BeautifulSoup

class scraper:

    def __init__(self, url):
        self.url = url

    def scrape(self, class_name, tag):
        website_url = requests.get(self.url).text      
        soup = BeautifulSoup(website_url,'lxml')
        my_table = soup.find('table',{'class':class_name})
        table_rows = my_table.findAll(tag)
        return table_rows

def wrangle_list (list):
    
    df = pd.DataFrame(columns = ['Year', 'Births', 'Deaths', 'Clinic'])
    Year = []
    Births = []
    Deaths = []
    Clinic = []

    for i in range(2,8):
            Year.append(list[i].findAll('td')[0].string)
            Births.append(list[i].findAll('td')[1].string)
            Deaths.append(list[i].findAll('td')[2].string)
            Clinic.append('First')
            Year.append(list[i].findAll('td')[0].string)
            Births.append(list[i].findAll('td')[5].string)
            Deaths.append(list[i].findAll('td')[6].string)
            Clinic.append('Second')

    df['Year'] = Year
    df['Births'] = Births
    df['Deaths'] = Deaths
    df['Clinic'] = Clinic

    return df

def wrangle_list2 (list):
    
    df = pd.DataFrame(columns = ['Year', 'Births', 'Deaths'])
    Year = []
    Births = []
    Deaths = []

    for i in range(1,len(list)):
            if (i<=24):
                Year.append(list[i].findAll('span')[0].string)
            else:
                Year.append(list[i].findAll('td')[1].string)
            Births.append(list[i].findAll('td')[2].string)
            Deaths.append(list[i].findAll('td')[3].string)
                    
    df['Year'] = Year
    df['Births'] = Births
    df['Deaths'] = Deaths
    
    return df

def remove_line_breaks (df):
    for i in df.columns:
        for j in range(len(df)):
             df.loc[j,i] = df.loc[j,i].strip()

def remove_comma (column):
    for x in range(len(column)):
        column[x]  = column[x].replace(',','')
    return column

# ''' Scrape yearly data '''

# website = scraper('https://en.wikipedia.org/wiki/Ignaz_Semmelweis')

# scraped_list = website.scrape('wikitable', 'tr')   

# wrangled_list = wrangle_list(scraped_list)

# remove_line_breaks(wrangled_list)

# remove_comma(wrangled_list['Births'])

# wrangled_list['Year'] = wrangled_list['Year'].apply(pd.to_datetime)

# wrangled_list[['Births', 'Deaths']] = wrangled_list[['Births', 'Deaths']].apply(pd.to_numeric)   

# ''' Scrape monthly data '''

# website2 = scraper('https://en.wikipedia.org/wiki/Historical_mortality_rates_of_puerperal_fever')

# scraped_list2 = website2.scrape('wikitable sortable', 'tr')

# wrangled_list2 = wrangle_list2(scraped_list2)

# remove_line_breaks(wrangled_list2)

# wrangled_list2 = wrangled_list2[wrangled_list2['Births']!='na']

# wrangled_list2['Year'] = wrangled_list2['Year'].apply(pd.to_datetime)

# wrangled_list2[['Births', 'Deaths']] = wrangled_list2[['Births', 'Deaths']].apply(pd.to_numeric)   

# wrangled_list2.reset_index(drop=True, inplace = True)

# print(wrangled_list2)
