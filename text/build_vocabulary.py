#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

Description: 

    Builds the corpus vocabulary from the word stream file 
    and based on stop words and MIN_WORD_FREQUENCY

Created on: Jun 28, 2011

@author: Clint P George

'''
from collections import defaultdict


MIN_WORD_FREQUENCY = 5
MIN_WORD_LENGTH = 3

def build_vocabulary(word_stream_file, vocab_file, freq_file, stopwords):
    
    vocab_dic = defaultdict(int); 

    with open(word_stream_file, "r") as fWS:
        for line in fWS:
            tokens = line.strip().split(" ")
            tokens = [w.strip().replace('\"', '').replace('\'', '').replace('`', '').replace('(', '').replace(')', '').rstrip('.').rstrip(',').lower() for w in tokens]
            content = [w for w in tokens if w not in stopwords] # removes stop words from vocab 
            for token in content:
                vocab_dic[token] += 1
    
    items = [(v, k) for k, v in vocab_dic.items()]
    items.sort()
    items.reverse()            
    items = [(k, v) for v, k in items]
    
    with open(vocab_file, "w") as f_vocab:
        with open(freq_file, "w") as f_freq:
            for k, v in items:
                f_freq.write(k + " " + str(v) + "\n")
                if v >= MIN_WORD_FREQUENCY and len(k) >= MIN_WORD_LENGTH: 
                    f_vocab.write(k + "\n")





'''
   Function main:
'''

if __name__ == '__main__':
    
    word_stream_file = raw_input("Word steam file: ") 
    vocab_file = raw_input("Vocabulary file: ") 
    freq_file = raw_input("Frequencies file: ") 
    
    stopwords = list();
    sw_file = raw_input("Stop words file: ")
    with open(sw_file, "r") as fSW: 
        for line in fSW: 
            stopwords.append(line.strip())
    

    build_vocabulary(word_stream_file, vocab_file, freq_file, stopwords)
