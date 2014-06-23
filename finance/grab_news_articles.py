#! /usr/bin/python
# -*- coding: utf-8 -*-

'''

Description: 
    This script grabs web text from the given URL input   
    It expects a input file with each line in the following format:  
    
    [ticker] | [date] (e.g. Fri, 15 Jul 2011 15:25:29 GMT) | 
    [header] (e.g. Summary of Second Quarter Margins for S&P 500 Stocks by Sectors) | [url]     
    
Dependency: 
    Python 2.6
    
Created on:
    July 13, 2011 
    
Author: 
    Clint P. George 

'''


import time
import os 
import string
import urllib2

from pyparsing import *
from lxml.html import fromstring
from lxml.html.clean import Cleaner
from optparse import OptionParser


def pyparsing_html_cleaner(targetHTML):

    removeText = replaceWith("")
    scriptOpen,scriptClose = makeHTMLTags("script")
    scriptBody = scriptOpen + SkipTo(scriptClose) + scriptClose
    scriptBody.setParseAction(removeText)
    
    anyTag,anyClose = makeHTMLTags(Word(alphas,alphanums+":_"))
    anyTag.setParseAction(removeText)
    anyClose.setParseAction(removeText)
    htmlComment.setParseAction(removeText)
    
    commonHTMLEntity.setParseAction(replaceHTMLEntity)
    
    # first pass, strip out tags and translate entities
    firstPass = (htmlComment | scriptBody | commonHTMLEntity | anyTag | anyClose ).transformString(targetHTML)
    
    # first pass leaves many blank lines, collapse these down
    repeatedNewlines = LineEnd() + OneOrMore(LineEnd())
    repeatedNewlines.setParseAction(replaceWith("\n"))
    secondPass = repeatedNewlines.transformString(firstPass)
    
    return secondPass

def lxml_html_cleaner(html): 

    doc = fromstring(html)
    
    tags = ['h1','h2','h3','h4','h5','h6', 'p',
           'div', 'span', 'img', 'area', 'map']
    args = {'meta':True, 'safe_attrs_only':False, 'page_structure':False, 
           'scripts':True, 'style':True, 'links':True, 'remove_tags':tags}

    cleaner = Cleaner(**args)
    
    path = '/html/body'
    body = doc.xpath(path)[0]
    
    return cleaner.clean_html(body).text_content().encode('ascii', 'ignore')


def make_valid_name(file_name):

    valid_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
    
    return ''.join(c for c in file_name if c in valid_chars)


def download_raw_html(input_file_name, output_dir, verbose):
    
    with open(input_file_name, "r") as fp:
        count = 0
        for article_line in fp:
            count += 1
            ss = article_line.strip().split('|')
            
            
            # Creates a new directory for date  
            
            tm = time.strptime(ss[1].strip(), "%a, %d %b %Y %H:%M:%S GMT")
            dir_name = time.strftime('%Y%m%d', tm)
            if not os.path.exists(os.path.join(output_dir, dir_name)):
                os.makedirs(os.path.join(output_dir, dir_name))
                if verbose: 
                	print 'Created dir: ', os.path.join(output_dir, dir_name)
            
            # Creates a new directory for ticker   
            
            ticker = ss[0].strip()
            if not os.path.exists(os.path.join(output_dir, dir_name, ticker)):
                os.makedirs(os.path.join(output_dir, dir_name, ticker))
                if verbose: 
                	print 'Created dir: ', os.path.join(output_dir, dir_name, ticker)            
            
    
            try:    
                if verbose: 
                	print 'Processing ', ss[0], ss[2], '...'
                html = urllib2.urlopen(ss[3]).read()
                file_name = make_valid_name(ss[2].strip())
                with open(os.path.join(output_dir, dir_name, ticker, file_name  + ".html"), 'w') as fp:
                    fp.write(html)                    
                with open(os.path.join(output_dir, dir_name, ticker, file_name  + ".txt"), 'w') as fc:
                    fc.write(lxml_html_cleaner(html))
#                with open(os.path.join(output_dir, dir_name, ticker, file_name  + ".txt2"), 'w') as fc2:
#                    fc2.write(pyparsing_html_cleaner(html))                      
                
                if verbose: 
                	print 'Finished processing ', ss[0], ss[2], '. Please wait(5s)...' 
                
            except: 
                if verbose: 
                	print 'Processing ', ss[0], ss[2], 'failed'
            
            time.sleep(5)
            



if __name__ == '__main__':
    '''
    Main function: 
    
    Example: 
    	python2.6 grab_news_articles.py -- help
    	python2.6 grab_news_articles.py -f /home/clint/Yahoo/20110725.txt -d /home/clint/Yahoo/rawdata
    '''    
    parser = OptionParser()
    parser.add_option("-f", dest="url_file", action="store", help = "URL file, where we store the html links")
    parser.add_option("-d", dest="download_dir", action="store", default = "./rawdata", help = "output directory, default ./rawdata")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")    
    (options, args) = parser.parse_args()
    
    if not os.path.exists(options.download_dir):
        os.makedirs(options.download_dir)
    
    download_raw_html(options.url_file, options.download_dir, options.verbose)
            
            
