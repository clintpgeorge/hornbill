'''
Created on Jun 29, 2011

@author: clint
'''
from collections import defaultdict

MIN_DOCUMENT_WORD_COUNT = 5
MIN_DOCUMENT_UNIQUE_WORD_COUNT = 3

def build_ldac_documents(word_stream_file, vocab_file, ldac_doc_file):
    '''
    creates the document word instances file from 
    the word stream file and vocabulary  
    '''
    vocab_dic = defaultdict(int);   
    wordid = 0; 
    vocab_list = list();
    with open(vocab_file, "r") as fVocab:
        for line in fVocab:
            token = line.strip()
            vocab_list.append(token)
            vocab_dic[token] = wordid 
            wordid += 1 
    
    print "Number of terms in the vocabulary: " + str(wordid)
    
    num_line_count = 0
    num_valid_docs = 0
    num_word_instances = 0
    with open(word_stream_file, "r") as fWS:
        with open(ldac_doc_file, "w") as fDW:
            for line in fWS:
                tokens = line.strip().split(" ")
                content = [w for w in tokens if w.lower() in vocab_list] 
                num_line_count += 1

                # if the document-word-counts are less than predefined 
                # threshold we ignore that document 
                if len(content) >= MIN_DOCUMENT_WORD_COUNT:
                    
                    doc_dic = defaultdict(int); 
                    for token in content:
                        doc_dic[token] += 1
                    
                    if doc_dic.__len__() >= MIN_DOCUMENT_UNIQUE_WORD_COUNT:

                        num_valid_docs += 1
                        num_word_instances += len(content)
                        
                        strLine = str(doc_dic.__len__()) + " "
                        for k, v in doc_dic.items():
                            strLine += str(vocab_dic[k]) + ":" + str(v) + " "
                        
                        fDW.write(strLine + "\n")
                    
    print "Number of documents read: " + str(num_line_count)
    print "Number of documents converted: " + str(num_valid_docs)
    print "Number of word instances: " + str(num_word_instances)


if __name__ == '__main__':

    word_stream_file = raw_input("Input: word steam file: ") 
    vocab_file = raw_input("Input: vocabulary file: ") 
    ldac_doc_file = raw_input("Output: ldac documents file: ") 

    build_ldac_documents(word_stream_file, vocab_file, ldac_doc_file)
