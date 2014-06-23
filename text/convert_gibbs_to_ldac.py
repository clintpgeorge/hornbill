#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from collections import defaultdict

'''

   This program converts a data file in Gibbs 
   sampling format to LDA-C format:
   
'''

if __name__ == '__main__':
    
    giibs_file_name = raw_input("File name (in Gibbs format): ")
    ldac_file_name = raw_input("Output file name: ")
    
    OFFSET = 1; # LDA-C format starts with 0 
    line_count = 0 
    doc_count = 0
    word_counts = defaultdict(int)
    num_unique_words = 0
    prev_did = "-1"
    
    with open(giibs_file_name, "r") as fg:
        with open(ldac_file_name, "w") as fo:
            
            for line in fg:
                line_count += 1
                la = line.strip().split(" ")
                
                if la[0] != prev_did: # new document 
                    
                    if doc_count > 0:
                        out_line = str(word_counts.__len__()) + " "
                        for k, v in word_counts.items():
                            out_line += str(k - OFFSET) + ":" + str(v) + " "
                        fo.write(out_line + "\n") 
                        word_counts.clear()
                        
                    doc_count += 1
                    prev_did = la[0]
                
                word_counts[int(la[1])]  += 1

            if doc_count > 0: # writes the last line 
                out_line = str(word_counts.__len__()) + " "
                for k, v in word_counts.items():
                    out_line += str(k - OFFSET) + ":" + str(v) + " "
                fo.write(out_line + "\n")  
                   
    print "Number of lines read: " + str(line_count)
    print "Number of documents: " + str(doc_count)
    
    
                
                
                
                            