#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from collections import defaultdict

'''

   This program converts a data file in sparse matrix  
   format to LDA-C format:
   
'''

if __name__ == '__main__':
    
    sm_file_name = raw_input("file name (in sparse matrix format): ")
    ldac_file_name = raw_input("output file name: ")
    
    OFFSET = 1; # LDA-C format starts with 0 
    line_count = 0 
    doc_count = 0
    num_unique_words = 0
    prev_did = "-1"
    
    with open(sm_file_name, "r") as fg:
        with open(ldac_file_name, "w") as fo:
            
            for line in fg:
                
                line_count += 1
                if line_count <= 3: continue # skip first three lines 
                
                la = line.strip().split(" ")
                
                if la[0] != prev_did: # new document 
                    
                    if doc_count > 0:
                        out_line = str(num_unique_words) + " " + out_line
                        fo.write(out_line + "\n") 
                    
                    doc_count += 1
                    prev_did = la[0]
                    out_line = str(int(la[1]) - OFFSET) + ":" + la[2] + " "
                    num_unique_words = 1
                
                else:
                    
                    out_line += str(int(la[1]) - OFFSET) + ":" + la[2] + " "
                    num_unique_words += 1 
                

            if doc_count > 0: # writes the last line 
                out_line = str(num_unique_words) + " " + out_line
                fo.write(out_line + "\n")
                   
    print "Number of lines read: " + str(line_count)
    print "Number of documents: " + str(doc_count)
    
    