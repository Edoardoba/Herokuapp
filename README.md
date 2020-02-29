# Herokuapp

The main idea of the project is to develop an Android application able to accurately predict house prices for the Roman rural area. This will take some parameters as inputs (such as total Area, Floor, Neighborhood...) and elaborate an estimate of the house price. This will be performed in differents steps. 

## Web Scraping

The first issue came with the database itself because I wasn't able to find a proper one (the only one which could have been reliable wasn't free). The only solution for that was to make a database on my own. I web-scraped directly from one of the most famous italian real estate agency website: [Immobiliare.it](https://www.immobiliare.it/). I retrieved some insight of every apartment (around 9000) in order to make an accurate prediction.

After having obtained the data, I also had to clean the records because there were some houses for which the price was not defined properly("Prezzo su richiesta"). All the code used is avalaible in the **heroku-webscraping.py** file. This is a preview of the Database itself.

<p align="center">
  <img width="460" height="400" src="https://i.ibb.co/cNBKGQX/Cattura.png">
</p>

## Building a model 

The following step was to build a model able to correctly predict the house prices. I have implemented *Linear regression*, through the sklearn Library in Python. The code is avalaible in the INSERIRE QUI file. 
