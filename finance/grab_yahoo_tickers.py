#! /usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'gian paolo ciceri <gp.ciceri@gmail.com>'
__version__ = '0.1'
__date__ = '20070401'
__credits__ = "queue_ and MT code was shamelessly stolen from pycurl example retriever-multi.py"

#
# Usage: 
#     python grab_yahoo_tickers.py -h 
#
# Description: 
#     To get tickers's information from Yahoo. 
#
# Input file format: 
#     <ticker> [tab] <company name> [tab] .. 
#     e.g. ADBE    Adobe Systems Inc    Information Technology    San Jose, California    

import sys, threading, Queue, datetime, os 
import urllib
import traceback
import time 
from optparse import OptionParser


# This thread ask the queue_ for job and does it!

class WorkerThread(threading.Thread):
    
    def __init__(self, queue):
        
        threading.Thread.__init__(self)
        self.queue_ = queue
        
        
    def run(self):
        
        while 1:
            # fetch a job from the queue_
            try:
                ticker, fromdate, todate = self.queue_.get_nowait()
            except Queue.Empty:
                raise SystemExit
            
            quote = dict()
            quote['s'] = ticker
            quote['d'] = str(int(todate[4:6]) - 1)
            quote['e'] = str(int(todate[6:8]))
            quote['f'] = str(int(todate[0:4]))
            quote['g'] = "d" 
            quote['a'] = str(int(fromdate[4:6]) - 1)
            quote['b'] = str(int(fromdate[6:8]))
            quote['c'] = str(int(fromdate[0:4]))
            #print quote
            
            params = urllib.urlencode(quote)
            params += "&ignore=.csv"

            url = "http://ichart.yahoo.com/table.csv?%s" % params
            
            if options.verbose:
                print "fetching:", ticker, url          
                
            if single_file:  # Store into a single file 
                with open(file_name, "a") as fp:                
                    try:
                        days = urllib.urlopen(url).readlines()
                        data = [day[:-2].split(',') for day in days]
                        list_count = 0
                        for day in data: # day = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos']
                            list_count += 1
                            if list_count == 1: continue
                            line = ticker
                            for item in day: line += ", " + item
                            fp.write(line + "\n")
                    except:
                        traceback.print_exc(file=sys.stderr)
                        sys.stderr.flush()
            
            else: # Store into multiple files 
                if ticker[0] == "^": 
                    tick = ticker[1:]
                else: 
                    tick = ticker
                ind_file_name = os.path.join(download_dir, "%s_%s.csv" % (tick, todate))
                with open(ind_file_name, "a") as fp:                
                    try:
                        fp.write(urllib.urlopen(url).read())
                    except:
                        traceback.print_exc(file=sys.stderr)
                        sys.stderr.flush()
                        
            
            if options.verbose:
                print ticker, url, "...fetched"
            else:
                sys.stdout.write(".")
                sys.stdout.flush()

            time.sleep(10)

if __name__ == '__main__':
    
    # Parse arguments

    single_file = False

    parser = OptionParser()
    
    to_date = datetime.datetime.now().strftime("%Y%m%d")
    from_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    parser.add_option("-f", "--file", dest="tickerfile", action="store", default = "./tickers.txt", help = "read ticker list from file, it uses ./tickers.txt as default")
    parser.add_option("-c", "--concurrent", type="int", dest="connections", default = 10, action="store", help = "# of concurrent connections")
    parser.add_option("-d", "--dir", dest="download_dir", action="store", default = "./rawdata/", help = "save date to this directory, it uses ./rawdata/ as default")
    parser.add_option("-t", "--to_date", dest="to_date", default = to_date, action="store", help = "most recent date needed")
    parser.add_option("-s", "--from_date", dest="from_date", default = from_date, action="store", help = "start date needed")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")	
    parser.add_option("-l", "--single_file", dest="single_file", action="store_true", help = "save outputs to a single file")			 
    (options, args) = parser.parse_args()

    tickerfile = options.tickerfile
    download_dir = options.download_dir
    connections =  options.connections
    to_date = options.to_date
    from_date = options.from_date
    single_file = options.single_file
    

    # Get input list
    
    try:
        tickers = open(tickerfile).readlines()
    except:
        parser.error("ticker file %s not found" % (tickerfile,))
        raise SystemExit
   
    
    
    # Build a queue with (ticker, from date, to date) tuples
    
    queue = Queue.Queue()
    for tickerRow in tickers:
        tickerRow = tickerRow.strip()
        if not tickerRow or tickerRow[0] == "#": continue
        tickerSplit = tickerRow.split("\t")
        queue.put((tickerSplit[0], from_date, to_date)) # ticker, from date, to date


    
    # Check arguments
    assert queue.queue, "No tickers given"
    numTickers = len(queue.queue)
    connections = min(connections, numTickers)
    assert 1 <= connections <= 255, "Too much concurrent connections asked"

    
    if options.verbose:
        print "----- Getting", numTickers, "tickers using", connections, "simultaneous connections -----\n"
        print "Start date: %s end date: %s" % (from_date, to_date)
    
    # Start a bunch of threads, passing them the queue_ of jobs to do
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    if single_file: 
        file_name = os.path.join(download_dir, "%s.csv" % (to_date,))
        with open(file_name, "w") as fp:
            fp.write('Ticker, Date, Open, High, Low, Close, Volume, Adj Clos\n')
        
    threads = []
    for dummy in range(connections):
        t = WorkerThread(queue)
        t.start()
        threads.append(t)
    
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    sys.stdout.write("\n")
    sys.stdout.flush()

    # Tell something to the user before exiting
    if options.verbose:	   
        print "All threads are finished - Good bye."
