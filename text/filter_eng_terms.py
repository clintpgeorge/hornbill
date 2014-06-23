'''
Created on Jul 22, 2011

@author: clint
'''

import enchant


if __name__ == '__main__':
    input_file = raw_input("input vocabulary file: ") 
    output_file = raw_input("output file: ") 
    
    
    eng_dict = enchant.Dict("en_US")
    
    with open(input_file, 'r') as fi:
        with open(output_file, 'w') as fo: 
            
            ignore_count = 0
            total = 0
            for word in fi: 
                total += 1
                if not eng_dict.check(word.strip()):
                    fo.write(word.strip() + '\n')
                else:
                    ignore_count += 1 
    
    print 'removed', ignore_count, 'eng words out of', total, 'words'
    
    