
# coding: utf-8

# # Web Scraping
# 
# Since we do not have a proper Db for the apartments in the Roman Area, I am going to web-scrape directly from one of the most famous italian real estate agency website: [Immobiliare.it](https://www.immobiliare.it/). I am going to retrieve some insight of every apartment (around 9000) in order to make an accurate prediction.

# In[4]:


import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import string
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.tokenize import RegexpTokenizer
import math
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import collections
from collections import defaultdict
import os


# In[276]:


def web_scrap(): 
    print ("Start : %s" % time.ctime())  #Just to see the time
    url="https://www.immobiliare.it/vendita-case/roma/?pag="
    counturl=1
    df=[]
    ndocs=int(12000/25)
    titles=[]
    descriptions=[]
    prices=[]
    locali=[]
    sup=[]
    bath=[]
    piano=[]
    zona=[]
    while counturl<=ndocs:
        housesites=[]
        goodurl=url+str(counturl)
        page = requests.get(goodurl)
        #web_soup = soup(requests.get(url, verify=False).text)
        soup = BeautifulSoup(page.content, 'html.parser')
        for a in soup.find_all('a', href=True,title=True,id=True):  #With this I get all the links of the page corresponding to houses
            housesites.append(a['href'])
        for a in housesites:
            time.sleep( 0.005 )
            try:
                page = requests.get(a)
                soup = BeautifulSoup(page.content, 'html.parser')
                check=soup.find_all('span',attrs = {'class':'text-bold'})[0].get_text() 
                if "€" in check:
                    a=soup.find_all('h1',attrs = {'class':'raleway title-detail'})[0].get_text()
                    if "asta" in a:
                        next
                    else:
                        #b=soup.find_all('div',attrs = {'class':'col-xs-12 description-text text-compressed'})[0].get_text()
                        c=soup.find_all('li' ,attrs={'class':'features__price'})[0].get_text()
                        d=soup.find_all('span',attrs = {'class':'text-bold'})[1].get_text() 
                        e=soup.find_all('span',attrs = {'class':'text-bold'})[2].get_text()
                        f=soup.find_all('span',attrs = {'class':'text-bold'})[3].get_text()
                        g=soup.find_all('abbr',attrs = {'class':'text-bold im-abbr'})[0].get_text()
                        h=soup.find_all('span',attrs = {'class':'im-address__content js-map-address'})[0].get_text()
                        c=c.replace("€","")
                        g=g.replace("\n","")
                        #b=b.replace("\n","")
                        g=g.replace("T","0")
                        h=h.replace("\n","")
                        while "-" in h:
                            h=h[h.find('-'):]
                            h=h[1:]
                            h=h.strip()
                        #h=line.split("-")[1]
                        #titles.append(a)
                        zona.append(h)
                        #descriptions.append(b)
                        prices.append(c)
                        locali.append(d)
                        sup.append(e)
                        bath.append(f)
                        piano.append(g)

                else:
                    a=soup.find_all('h1',attrs = {'class':'raleway title-detail'})[0].get_text()
                    if "asta" in a:
                        next
                    else:
                        #b=soup.find_all('div',attrs = {'class':'col-xs-12 description-text text-compressed'})[0].get_text()
                        c=soup.find_all('li' ,attrs={'class':'features__price'})[0].get_text()
                        d=soup.find_all('span',attrs = {'class':'text-bold'})[0].get_text() 
                        e=soup.find_all('span',attrs = {'class':'text-bold'})[1].get_text()
                        f=soup.find_all('span',attrs = {'class':'text-bold'})[2].get_text()
                        g=soup.find_all('abbr',attrs = {'class':'text-bold im-abbr'})[0].get_text()
                        h=soup.find_all('span',attrs = {'class':'im-address__content js-map-address'})[0].get_text()
                        #b=b.replace("\n","")
                        c=c.replace("€","")
                        g=g.replace("\n","")
                        h=h.replace("\n","")
                        while "-" in h:
                            h=h[h.find('-'):]
                            h=h[1:]
                            h=h.strip()
                        g=g.replace("T","0")
                        #h=line.split("-")[1]
                        #titles.append(a)
                        #descriptions.append(b)
                        prices.append(c)
                        locali.append(d)
                        sup.append(e)
                        bath.append(f)
                        piano.append(g)
                        zona.append(h)

            except:
                next
        counturl+=1
    data_tuples = list(zip(locali,sup,bath,piano,zona,prices))
    df=pd.DataFrame(data_tuples,columns = ["Locals","Area","Bath","Floor",'Zone',"Price"])
    

    print ("End : %s" % time.ctime())
    return(df)


# In[277]:


df=web_scrap()


# In[10]:


#9100 elements retrieved
df


# In[16]:


df=pd.read_csv(r'heroku.csv')


# # Data cleaning
# 
# Since there are some typos in the columns extracted, we clean up those columns.

# In[17]:


def clean_information(df): 
    
    #df = pd.read_pickle("housesfinal")
    # We remove \xa0 from these columns:
    df['Locals'] = df['Locals'].astype(str).str.replace(u'\xa0', '')
    df['Bath'] = df['Bath'].astype(str).str.replace(u'\xa0', '')
    df['Floor'] = df['Floor'].astype(str).str.replace(u'\xa0', '')
    # We remove spaces in these columns:
    df['Price'] = df['Price'].astype(str).str.strip()
    df['Floor'] = df['Floor'].astype(str).str.strip()
    # We remove dots in Prices column so, later, we can transform string array to number array:
    df['Price'] = df['Price'].str.replace('.', '')
    # We drop rows with non numeric symbols (es. A in Floor column or 3+ in Locals and Bath columns):
    df = df[ df.Price.apply(lambda x: x.isnumeric())]
    # index of rows from zero to len(df)
    df.index = np.arange(0,len(df))
    return df

df=clean_information(df)


# In[18]:


#15 rows cut out because price reported was "Prezzo su richiesta"

df


# In[19]:


df.to_csv(r'heroku_for_regression.csv', index = False)

