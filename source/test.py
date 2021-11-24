
from POS_tagging import HMM_Viterbi
from POS_tagging.HMM_Viterbi import pos_tagging_HMM_viterbi
from WS_dict_MM.dict_MM import MM
from WS_static_n_gram.stat_LM import n_garm, load_grams
import numpy as np
import json
import time

from POS_tagging import *
from WS_dict_MM import *

#---------------------
#configuration
# 1:ngram 2:MM
ws_method = 1
testpath = "D:\\resource\\STUDY\\NLP\\test_set.txt"



#---------------------------------


def prepare():
    load_grams()



if __name__ == '__main__':
    prepare()
    testfile = open(testpath,"r")
    my_count = 0
    correct_count = 0
    answer_count = 0
    p = 0
    r = 0
    f1 = 0
    s_time = time.perf_counter()

    total_test_num = 5
    for i in range(total_test_num):
        try:

            sentense = testfile.readline().strip()
            answer_split = eval(testfile.readline().strip())
            answer_class = eval(testfile.readline().strip())

            answer_count+=len(answer_split)

            my_ws_re = MM(sentense)
            my_count += len(my_ws_re)

            my_pos_re = pos_tagging_HMM_viterbi(answer_split)
            print("my_ws_re",my_ws_re)

            print("answer split",len(answer_split),answer_split)

            print("my_pos_re",len(my_pos_re),my_pos_re)
            print("answer class",len(answer_class),answer_class)

            for (index,c_class) in enumerate(my_pos_re):
                cur_word = c_class[0]
                cur_class = c_class[1]

                cur_answer_index = answer_split.index(cur_word)
                cur_answer_class = answer_class[cur_answer_index]

                if cur_class == cur_answer_class:
                    correct_count += 1



        except:
            continue

    e_time = time.perf_counter()
    print("total_time for ",total_test_num, " is : ",e_time-s_time)
    p = correct_count/my_count
    r = correct_count / answer_count
    f1 = 2*p*r / (p+r)
    print("over")
    print(p,r,f1)
