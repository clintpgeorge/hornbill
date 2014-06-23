#! /usr/bin/python
# -*- coding: utf-8 -*-
'''

Description: 
    This script grabs Yahoo financial news meta data from 
    the Yahoo financial news services and for a given ticker 
    name and company. It expects a ticker file with 
    each line in the following format 
    
    [ticker] [tab] [company name] [tab] [section] [tab] [place] 
    
    e.g. ADBE    Adobe Systems Inc    Information Technology    San Jose, California       
    
Dependency: 
    Python 2.6

Help: 
    python2.6 grab_yahoo_news_metadata.py --help 
    
Created on:
    July 11, 2011 
    
Author: 
    Clint P. George 

'''


import feedparser
import socket
import sys
import Queue, datetime, os 
import urllib
import time
import string

from optparse import OptionParser

timeout = 120 # sets time out interval 
socket.setdefaulttimeout(timeout)


def make_valid_name(file_name):
    valid_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in file_name if c in valid_chars)


def grab_yahoo_news_metadata(queue):
    
    while 1:
        
        if queue.empty(): break 
        
        # Fetch a job from the queue        
        try:
            (ticker, company, start_date, end_date) = queue.get() 
        except Queue.Empty:
            break
        
        try:         

            tm_from = time.strptime(start_date, "%Y%m%d")
            tm_to = time.strptime(end_date, "%Y%m%d")
            
    
            # Creates URL         
            opt = dict()
            opt['s'] = ticker + ',' + company # query 
            feed_url = 'http://finance.yahoo.com/rss/headline?%s' % urllib.urlencode(opt)
            
            if options.verbose: 
                print ticker, ': fetching:', feed_url 
            
            d = feedparser.parse(feed_url)  
    
            articles = list()  
            count = 0
            valid_count = 0 
    
            for s in d.entries:
                count += 1 
                tm = time.strptime(s.updated.strip(), "%a, %d %b %Y %H:%M:%S GMT") # this our assumption
                if (tm_from < tm) and (tm < tm_to):
                    valid_count += 1
                    articles.append((s.updated.strip(), unicode(make_valid_name(s.title.strip())).encode("utf-8"), unicode(s.link).encode("utf-8")))
                    
            
            
            if single_file:  # Store into a single file 
                ind_file_name = os.path.join(download_dir, "%s.txt" % (end_date,))
            else: # Store into multiple files 
                if ticker[0] == "^": tick = ticker[1:]
                else: tick = ticker
                ind_file_name = os.path.join(download_dir, "%s_%s.txt" % (tick, end_date))
    
            
            
            if valid_count > 0:            
                with open(ind_file_name, "a") as fp:                
                    for article in articles: 
                        fp.write(ticker + "|" + article[0].strip() + "|" + article[1].strip() + "|" + article[2] + "\n")
                        
                if options.verbose:    
                    print ticker, ' (', valid_count, '/', count, ') articles read.'
                else:
                    sys.stdout.write(".")
                    sys.stdout.flush()
            else: 
                if options.verbose: 
                    print ticker, 'no news articles found.' 

        except:
            print 'Failed to retrieve data for', ticker, company, sys.exc_info()
            
            
        time.sleep(5) # in order to reduce traffic 




if __name__ == '__main__':
    
    # python2.6 grab_yahoo_news_metadata.py -v -l -s 20110723 -e 20110724 -d /home/clint/Yahoo/
    
    # Parse arguments

    single_file = False
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    
    parser = OptionParser()
    parser.add_option("-f", dest="ticker_file", action="store", default = "./tickers.txt", help = "ticker list file, default ./tickers.txt")
    parser.add_option("-d", dest="download_dir", action="store", default = "./rawdata", help = "output directory, default ./rawdata")
    parser.add_option("-s", dest="start_date", default = start_date, action="store", help = "start date")
    parser.add_option("-e", dest="end_date", default = end_date, action="store", help = "end date")
    parser.add_option("-l", dest="single_file", action="store_true", help = "whether to save outputs to a single file")      
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")    
       
    (options, args) = parser.parse_args()

    ticker_file = options.ticker_file
    download_dir = options.download_dir
    end_date = options.end_date
    start_date = options.start_date
    single_file = options.single_file    

    
    # Get input list and build a queue 
    # with (ticker, from date, to date) tuples
    try:
        tickers = open(ticker_file).readlines() 
        queue = Queue.Queue()
        for tickerRow in tickers:
            tickerRow = tickerRow.strip()
            if not tickerRow or tickerRow[0] == "#": continue
            tickerSplit = tickerRow.split("\t")
            queue.put((tickerSplit[0], tickerSplit[1], start_date, end_date)) # ticker, company name, from date, to date
    except:
        parser.error("ticker file %s not found" % (ticker_file,))
        raise SystemExit
   
    
    # Check arguments
    assert queue.queue, "No tickers given"
    num_tickers = len(queue.queue)


    
    if options.verbose:
        print "----- Getting", num_tickers, "tickers -----\n"
    
   
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
            
    grab_yahoo_news_metadata(queue)
    
    if options.verbose:       
        print "Finished."
        
