"""
Created on Fri Sep  8 22:11:32 2017

@author: mincev
"""
import requests as r
import numpy as np
#note: if using spyder ide remember to set the console working directory to crawler_code
from helper import helper 

class NASDAQ_Crawler(object):
    """
    Downloads financial information from:
        "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=" \n
        + user_provided_exchange + "render=download"
    input: 
        exchange = user provided exchange name from which to download f.info
    """
    global URL_START, URL_END
    URL_START =  "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
    URL_END = '&render=download'
    
    def __init__(self, exchange = "NASDAQ"):
        assert type(exchange) is str
        self.exchange = exchange
    
    def download_text(self, repeat = 5):
        """
        input:
            repeat (int) = number of times url is tried
        output: 
            header = "Symbol","Name","LastSale","MarketCap","ADR TSO", \n
                     "IPOyear", "Sector","Industry","Summary Quote",
            text (str list) = donloaded data 
        """
        assert type(repeat) is int
        assert repeat > 0
        
        text = None
        header = None
        for _ in range(repeat):
            try:
                data = r.get(URL_START + self.exchange + URL_END)
                text = data.text.split('\n')
                header = text[0]
                if header and text is not None: break
            except:
               continue
        return(header, text[1:])
    
    def format_text(self, text):
        """
        input (str list):
            text (str list) = (eg: ouput from download_text())
        output (str list, dict):
            tickers = ticker list
            tickers_dict = information about ticker
            ipos_dict = tickers with ipos in dict years 
        """
        assert type(text) == list
        assert type(text[0]) == str

        tickers = []
        tickers_dict = {}
        ipos_dict = {}
        ipos_list = []
        for num, line in enumerate(text):
            line = line.strip().strip('"').split('","')
            if len(line) != 9: continue # filter unmatched format
            line[1] = line[1].replace(',', '').replace('.', '') #format company name
            ticker = line[0]
            ipo_year = line[5]
            #store ticker 
            tickers.append(ticker)
            #store information about ticker 
            tickers_dict[ticker] = line[1:]
            #store ticker in ipo year 
            if ipo_year not in ipos_list:
                ipos_list.append(ipo_year)
                ipos_dict[ipo_year] = []
            ipos_dict[ipo_year].append(ticker)
            
        return(tickers, tickers_dict, ipos_dict)

if __name__ == "__main__":
    #download data for "NASDAQ", "NYSE", "AMEX"
    headers = []
    exchanges = []
    financial_informations  = []
    for exchange in ["NASDAQ", "NYSE", "AMEX"]: 
        crawler = NASDAQ_Crawler(exchange)
        print("Crawling NASDAQ.com for "+exchange+ " please wait....\n")
        header, financial_information = crawler.download_text()
        
        if financial_information is not None:
            headers.append(header)
            exchanges.append(exchange)
            financial_informations.extend(financial_information)
    
    assert headers[0] == headers[1] == headers[2]    
    
    tickers, tickers_dict, ipos_dict = crawler.format_text(financial_informations)
    
    #save tickers and tickers_dict
    print("Saving data...")
    tickers = np.asarray(tickers)
    np.save("obj/tickers", tickers)
    helper.save_obj("NASDAQ_ticker_dict", tickers_dict)
    helper.save_obj("NASDAQ_ipo_dict", ipos_dict)
    print("\nData saved in obj folder")    