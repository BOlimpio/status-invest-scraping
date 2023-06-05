import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_stock_info(stock_code):
    url = f"https://statusinvest.com.br/fundos-imobiliarios/{stock_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting required information from the website
        p_vp = soup.find(text='P/VP').find_next(class_='value').text.strip()
        p_l = soup.find(text='P/L').find_next(class_='value').text.strip()
        dy = soup.find(text='DY').find_next(class_='value').text.strip()
        
        return {'Code': stock_code, 'P/VP': p_vp, 'P/L': p_l, 'DY': dy}
    else:
        print(f"Failed to retrieve data for stock {stock_code}")
        return None
