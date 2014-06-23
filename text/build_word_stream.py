#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Description: 
    This script will read text and tokenizes using 
    NLTK reg-ex module  

Created on: Jun 22, 2011

@author: Clint P. George 
'''

import os
import sys
from nltk.tokenize import regexp_tokenize


def build_word_stream(root_folder, ws_file, log_file):
    '''
    Read data from text files (space separated word) 
    and build a word stream 
    '''
    
    folder_count = 0
    file_count = 0
    
    with open(log_file, "w") as fl:
        with open(ws_file, "w") as fw:
            
            fl.write("docid,category,subject,wordcount\n")    
            
            for root, subFolders, files in os.walk(root_folder):
                
                folder_count += len(subFolders)
                for file in files:
                    file_count += 1
                    file_name = os.path.join(root, file)    
                
                    with open(file_name, "r") as fp:
                        try:
                            tokens = list()
                            for each_line in fp: 
                                la = each_line.strip().split(" ")
                                for term in la: tokens.append(term)
                            
                            if len(tokens) > 0: 
                                for token in tokens: 
                                    fw.write(token + " ")    
                                fw.write("\n")    

                            fl.write(str(file_count) + "," 
                                     + os.path.basename(root) + "," 
                                     + os.path.relpath(file_name, root_folder) 
                                     + "," + str(len(tokens)) + "\n")               
                        except: 
                            fl.write(str(file_count) + "," 
                                     + os.path.basename(root) + "," 
                                     + os.path.relpath(file_name, root_folder) 
                                     +  " F \t\t text pre-processing failed : %s"
                                     + sys.exc_info() + "\n")

def tokenize_text(page_text):
    '''
    Tokenizes text using NLTK and regEx   
    '''

    pattern = r'''(?:[A-Z][.])+|([1-9]|1[0-2]|0[1-9]){1}(:[0-5][0-9][aApP][mM]){1}|([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})|[$?|\-?]\d[\d,.:\^\-/\d]*\d|((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)|\w+[\w\-\#\@\'.&$]*\w+|[\@|\#|\&]?\w+(\w+)?|[:punct:]'''
    remove_list = ["[", "]", "{", "}", "(", ")", 
              "'", ".", "..", "...", ",", "?", "!", 
              "/", "\"", "\"", ";", ":", "-", "�", "_", "�", "�", 
              "`", "~", "@", "$", "^", "|", "#", "=", "*", "?"];
    ## making it to lower case may affect the performance
    tokens = regexp_tokenize(page_text, pattern)

    ## Removes unnecessary words 
    wt = [w for w in tokens if ((w not in remove_list) and (len(w) > 1))];        

    return wt;
    


def tokenize_and_build_word_stream(root_folder, ws_file, log_file):
    '''
    Read data from text files (tokenize using regexp) 
    and build a word stream 
    '''
    
    folder_count = 0
    file_count = 0
    
    with open(log_file, "w") as fl:
        with open(ws_file, "w") as fw:
            
            fl.write("docid,category,subject,wordcount\n")    
            
            for root, subFolders, files in os.walk(root_folder):
                
                folder_count += len(subFolders)
                for file in files:
                    file_count += 1
                    file_name = os.path.join(root, file)    
                
                    with open(file_name, "r") as fp:
                        try:
                            page_text = ""
                            for each_line in fp: page_text += each_line
                                
                            tokens = tokenize_text(page_text)    
                            
                            if len(tokens) > 0: 
                                for token in tokens: fw.write(token + " ")    
                                fw.write("\n")    

                            fl.write(str(file_count) + "," 
                                     + os.path.basename(root) + "," 
                                     + os.path.relpath(file_name, root_folder) 
                                     + "," + str(len(tokens)) + "\n")               
                        except: 
                            fl.write(str(file_count) + "," 
                                     + os.path.basename(root) + "," 
                                     + os.path.relpath(file_name, root_folder) 
                                     +  " F \t\t text pre-processing failed : %s"
                                     + sys.exc_info() + "\n")


def tokenize_file(input_file, ws_file):
    '''
    Read data from the text file (tokenize using regexp) 
    and build a word stream 
    '''
    
    with open(ws_file, "w") as fw:
        with open(input_file, "r") as fp:
            for each_line in fp: 
                tokens = tokenize_text(each_line.strip())    
                if len(tokens) > 0: 
                    for token in tokens: fw.write(token + " ")    
                    fw.write("\n")    


if __name__ == '__main__':
    
    
    ## To build word stream from a text file 
    ## This text file represents the whole corpus 
    ## with each line a single document 
    ## Note: This approach is not suitable for large 
    ## documents  
    
#    input_file = raw_input("Corpus file: ") 
#    ws_file = raw_input("Word stream file: ") 
#    tokenize_file(input_file, ws_file)
    
    
    ## To build word stream from text files 
    
    
    rootFolder = raw_input("Input: data folder: ") # /home/cgeorge/Dropbox/lda-data/newman
    logFile = raw_input("Output: log file: ") # /home/cgeorge/Dropbox/lda-data/newman.log
    ws_file = raw_input("Output: word stream file: ") # /home/cgeorge/Dropbox/lda-data/newman.wordstream
    build_word_stream(rootFolder, ws_file, logFile) 
    
    
    
    
    