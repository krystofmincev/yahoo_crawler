#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:40:13 2017

@author: mincev

To do:
    #Write script for determining period_1 and period_2 given dates not \
    Yahoo indetifiers - use selenium to execute js 
    #Replace webbrowser with phantomJS selenium or requests 
"""
import os
import numpy as np
import pandas as pd
import webbrowser as wb
from helper import helper
from time import sleep

class YAHOO_Crawler(object):
    """
    Class for crawling technicals from yahoo finance:
    6 technicals (OPEN, CLOSE, ADJ_CLOSE, VOLUME, HIGH, LOW) \n
    are scraped for a given list of tickers
    
    Note: YAHOOs uses crumbs meaning that the URL_END may need to be changed later
    """
    global TIMEOUT, URL_START
    TIMEOUT = 10
    URL_START = "https://query1.finance.yahoo.com/v7/finance/download/"   
    
    def __init__(self, tickers, csv_path = "/home/mincev//Downloads/{0}.csv", 
                 period_1 = 600, period_2 = 3005944800, crumb = "tuH4UvUMPlH",
                 browser = "chrome"):
        """
        input:
            tickers (str list) = list of company tickers to download
            csv_path (str) = path to default downloads folder in drive
            period_1 (int) = YAHOO identifier for start date (used for download)
            period_2 (int) = Y.identifier that represents download end date 
            crumb (str) = YAHOO user identifier try access in browser (new window) \n
                            to get your crumb if default is not working
            browser (str) = used to open and kill tabs eg:firefox.exe \n
                            must end with .exe if in windows
        Output: 
            self.tickers = tickers list
            self.csv_path = download path 
            self.url_end = url donwloader to be added after (URL_START + ticker)
        """
        assert type(tickers) is list 
        assert type(tickers[0]) and type(csv_path) and type(browser) is str
        assert type(period_1) and type(period_2) is int
        assert csv_path[-4:] == ".csv"
        
        self.tickers = tickers
        self.csv_path = csv_path
        self.browser = browser
        self.url_end = "?period1=" + str(period_1) + "&period2=" + str(period_2) + \
                        "&interval=1d&events=history&crumb=" + crumb
            
    def download_data(self, ticker = ["NIKE"], repeat = 5):
        """
        Downloads techicals for 'ticker' from Yahoo Finance 
        Input:
            ticker (str) = yahoo ticker 
            repeat (int) = number of times to try accesing website
        Output:
            (bool) = True if data is downloaded and False otherwise
        """
        assert type(ticker) is str
        assert type(repeat) is int 
        
        print("Downloding data for "  + ticker)
        url = URL_START + ticker + self.url_end
        for i in range(repeat):
            if wb.open(url, autoraise=False): 
                #print("Successfully Downloaded Data for " + ticker + "\n")
                return True
            sleep(0.5)
            
        print("Unable to Download Data for " + ticker)
        print("-----------------------\n")
        return False

    def csv2dic(self, ticker, tick_dict = {}, remove_download = True):
        """
        Adds csv data as a list to a dictionary if available 
        Input:
            ticker (str) = company whos technicals shall be added to tick_dic
            tick_dict (dict)= ticker denominated dictionary [ticker][date][technicals]
        Output:
            tick_dict (dict) = see input - if found includes ticker technicals 
        """
        assert type(ticker) is str
        assert type(tick_dict) is dict
        
        counter = 0
        while not counter == TIMEOUT and not os.path.exists(self.csv_path.format(ticker)):
            sleep(1)
            counter += 1

        if counter == TIMEOUT:
            print("Could not find data for {0}".format(ticker))
            print("-------------------------\n")
            #close browser/tab
            if self.browser[-4:] == ".exe": #user on windows 
                os.system("taskkill /im " + self.browser + " /f")
            else: #user on linux
                browser = "chrome"
                os.system("pkill " + browser)
                os.system("pkill " + self.browser)
            return tick_dict
        
        date_dict = {}
        with open(self.csv_path.format(ticker)) as comp_file:
            data = pd.read_csv(comp_file, delimiter=',')
            
            #test case
            try:
                header = data.columns.values.tolist()
                assert len(header) is 7
                assert header[0] == 'Date'
            except:
                print("Incompatible data downloaded for {0}\n".format(ticker))
                print("-------------------------\n")
                return tick_dict
            
            
            print("Storing technicals in dictionary... \n")
            for technicals in data.values.tolist()[1:]:#removes header
                date_dict[technicals[0]] = technicals[1:]
        
        if remove_download:
            os.remove(self.csv_path.format(ticker))
        
        tick_dict[ticker] = date_dict
        return tick_dict

    def download_all_tickers(self):
        """
        Downloads technicals for a ticker list
        Input:
            self = all tickers 
        Output:
            tick_dict = a dictioanry of all technicals for all tickers \n
                        fomatted as tick_dict[ticker][date] = technicals
        """
        print("Commencing download for " + str(len(self.tickers)) + " tickers\n")
        tick_dict = {}
        try:
            for i, ticker in enumerate(self.tickers):
                if self.download_data(ticker):
                    tick_dict = self.csv2dic(ticker, tick_dict)
        except: 
            print("Error occured at ticker: " + ticker + " index: " + str(i))
            print("The generated dictionary up to this error is returned\n")
            return tick_dict
                
        return tick_dict

if __name__ == "__main__":
    tickers = np.load("obj/tickers.npy")
    tickers = tickers.tolist()
    
    #test cases
    test_crawler = YAHOO_Crawler(['PIH'])
    test_crawler_2 = YAHOO_Crawler(['ZZZZZz', 'ZzzZp'])
    helper.save_obj("technicals", test_crawler)
    try:
        assert len(test_crawler.download_all_tickers()) is not 0    
        assert len(test_crawler_2.download_all_tickers()) is 0  
    except:
        print("Test case failed...\nTry changing the class crumb or periods (1&2)") 
    crawler_obj = YAHOO_Crawler(tickers)
    tick_dict = crawler_obj.download_all_tickers()
    helper.save_obj("technicals", tick_dict)
    