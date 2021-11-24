#---------------------
#configuration
# 1:ngram 2:MM
from POS_tagging import HMM_Viterbi
from WS_static_n_gram.stat_LM import n_garm, load_grams

ws_method = 1



#---------------------------------
import numpy as np
import json

from POS_tagging import *
from WS_dict_MM import *

def prepare():
    load_grams()



if __name__ == '__main__':
    print("\n")
    print("-"*150)
    print("welcome to WYD_NLP 1.0 !")
    flag = eval(input("Please choose to deal with one sentence or one file  <1:sentence 2:file> : "))
    if flag == 1:
        ws_method = eval(input("choose your word split method <1:ngram  2:MM> ： "))
        sentence = input("now put your sentence  <请输入中文> : ")
        print("The WS and POS_tagging result is as follow: (in a minute please wait a little while )")
        prepare()
        word_list = n_garm(sentence=sentence,garm=2)
        #print("这是分词结果",word_list)
        re = HMM_Viterbi.pos_tagging_HMM_viterbi(wordlist=word_list)
        print(re)



    print("-" * 150)
    print("\n")

