from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped text-sm text-lg-normal'})
index = table.find_all('tr')
index[1].find_all('th', attrs={'class' : 'font-semibold text-center', 'scope':'row'})[0].text
index[1].find_all('td', attrs={'class' : 'text-center'})[0].text
index[1].find_all('td', attrs={'class' : 'text-center'})[1].text
index[1].find_all('td', attrs={'class' : 'text-center'})[2].text
index[1].find_all('td', attrs={'class' : 'text-center'})[3].text

tanggal = table.find_all('th', attrs={'class' : 'font-semibold text-center', 'scope':'row'})

row_length = len(tanggal)

temp = [] #initiating a list 

for i in range(1, row_length):

    #scrapping process
    #get Dates
    Date = index[i].find_all('th', attrs={'class' : 'font-semibold text-center', 'scope':'row'})[0].text
    Date = Date.strip()
    
    
    #get Market Cap
    MarketCap = index[i].find_all('td', attrs={'class' : 'text-center'})[0].text
    MarketCap = MarketCap.strip()
    
    
    #get Volume
    Volume = index[i].find_all('td', attrs={'class' : 'text-center'})[1].text
    Volume = Volume.strip()
    
    #get Open Values
    Open = index[i].find_all('td', attrs={'class' : 'text-center'})[2].text
    Open = Open.strip()
    
    #get Close Values
    Close = index[i].find_all('td', attrs={'class' : 'text-center'})[3].text
    Close = Close.strip()
    
    temp.append((Date, MarketCap,Volume,Open,Close))
     
temp = temp[::-1]

#change into dataframe
ethereum = pd.DataFrame(temp, columns = ('Date','MarketCap','Volume','Open','Close'))

#insert data wrangling here
ethereum['MarketCap'] = ethereum['MarketCap'].str.replace('$','')
ethereum['MarketCap'] = ethereum['MarketCap'].str.replace(',','')
ethereum['MarketCap'] = ethereum['MarketCap'].astype('int64')
ethereum['Volume'] = ethereum['Volume'].str.replace('$','')
ethereum['Volume'] = ethereum['Volume'].str.replace(',','')
ethereum['Volume'] = ethereum['Volume'].astype('int64')
ethereum['Open'] = ethereum['Open'].str.replace('$','')
ethereum['Open'] = ethereum['Open'].str.replace(',','')
ethereum['Open'] = ethereum['Open'].astype('float64')
ethereum['Close'] = ethereum['Close'].str.replace('$','')
ethereum['Close'] = ethereum['Close'].str.replace(',','')
ethereum['Close'] = ethereum['Close'].str.replace('N/A','2169.40')
ethereum['Close'] = ethereum['Close'].astype('float64')
ethereum['Date'] = ethereum['Date'].astype('datetime64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{ethereum["volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = ethereum.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)