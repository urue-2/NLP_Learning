# language model
import copy
import json
import  time
import random
import math
import numpy as np

lpls_p1 = random.uniform(0, 1)
lpls_p2 = random.uniform(0, 1)


fp = "D:\\resource\\STUDY\\NLP\\2014_corpus.txt"
corpus = open(fp,"r",encoding="utf-8")

gram1={}
gram1_max = 23
gram2={}
gram2_max = 29
gram3={}
gram3_max = 34


def load_grams():
    """

    :return: 载入json格式的 n-gram 模型
    """
    global gram1,gram2,gram3
    ft1 = "D:\\resource\\STUDY\\NLP\\2014_corpus_1gram.txt"
    ft2 = "D:\\resource\\STUDY\\NLP\\2014_corpus_2gram.txt"
    ft3 = "D:\\resource\\STUDY\\NLP\\2014_corpus_3gram.txt"
    with open(ft1, 'r')as f:
        gram1 = json.load(f)
    f.close()
    with open(ft2, 'r')as f:
        gram2 = json.load(f)
    f.close()
    with open(ft3, 'r')as f:
        gram3 = json.load(f)
    f.close()

def gen_graph(sentence):
    '''

    :param sentence:
    :return: 列表表示的图

    '''
    #print(sentence)
    sen_len = len(sentence)

    graph = [[] for i in range(sen_len)]
    #print(graph)
    total_layer_number = sen_len
    graph = [[] for i in range(total_layer_number)]



    cur_layer_index = 0

    open_table = [("B",0)] # 词和词在句子中的起始位置
    graph[0].append("BOS")

    while open_table!=[]:
        if open_table==[]:
            break
        cur_word = open_table[-1][0]
        cur_sen_index = open_table[-1][1]
        del open_table[-1]
        suu_nodes = []
        s_index = cur_sen_index+1
        e_index = min(s_index+gram1_max,sen_len-1)
        while not (s_index > e_index):
            test_gram = sentence[s_index:e_index+1]
            if test_gram in gram1.keys():
                suu_nodes.append((test_gram ,s_index))
            e_index -= 1

        if suu_nodes==[]:
            if cur_word=="E" or cur_sen_index == sen_len-2:
                break
            else:
                # min(sen_len,m+gram1_max)-1
                x = cur_sen_index+1
                m = x+1
                y = m
                test_gram = sentence[m:y+1]

                while test_gram not in gram1.keys():
                    if y!=sen_len+1:
                        y+=1
                    else:
                        m+=1
                        y=m
                    test_gram = sentence[m:y+1]

                #print(cur_word,"until",test_gram)

                for i in range(x,m):
                    can_word = sentence[i]
                    if can_word not in graph[i]:
                        graph[i].append(can_word)
                    #print(graph)


        else:
            for suu in suu_nodes:
                if suu[0] not in graph[suu[-1]]:
                    graph[suu[-1]].append(suu[0])
                open_table.append(suu)
                #print(graph)


    graph[-1]="EOS"
    #print(graph)
    return graph

def cal_distance(word1,word2):
    """

    :param word1:
    :param word2:
    :return: -log(p(word2|word1))
    """

    gram1_total_number = 15439391
    global lpls_p1,lpls_p2

    ffd = gram1.get(word1,{})
    f_word1 = 0
    for k in ffd.values():
        f_word1+=k

    f_w1_w2 = gram2.get(word1+"@"+word2,0)

    p = lpls_p1*(lpls_p2*(f_w1_w2/f_word1) + 1-lpls_p2 )  +  (1-lpls_p1)*( (f_word1+1) /gram1_total_number)
    return -math.log(p)

def viterbi(graph):
    """

    :param graph:
    :return: shortest path 即分词结果
    """
    total_layer_number = len(graph)

    # forward part
    short_path_index = [[] for i in range(total_layer_number + 1)]
    short_path_index[1].append([(0, 0), 0])
    for cur_layer_index in range(1, total_layer_number):


        short_path_index[cur_layer_index].sort(key=lambda x: x[1])
        del short_path_index[cur_layer_index][1:]


        my_pre_record = short_path_index[cur_layer_index][0]
        my_pre = graph[my_pre_record[0][0]][my_pre_record[0][1]]

        my_pre_shorest_dis = my_pre_record[1]

        node_num = len(graph[cur_layer_index])
        print(cur_layer_index , my_pre)


        for in_layer_index in range(node_num):
            cur_node = graph[cur_layer_index][in_layer_index]
            print("in",str(cur_layer_index),cur_node,my_pre)


            new_dis = my_pre_shorest_dis + cal_distance(my_pre,cur_node)
            next_layer_index = cur_layer_index + len(cur_node)

            if next_layer_index == total_layer_number:
                break


            short_path_index[next_layer_index].append([(cur_layer_index,in_layer_index),new_dis])


        #print("after",str(cur_layer_index),short_path_index)


    print("中间部分",short_path_index)

    # backward part

    re = []
    layer_index = total_layer_number-1


    while layer_index!=1:
        my_pre_layer_index = short_path_index[layer_index][0][0][0]
        my_pre_inlayer_index = short_path_index[layer_index][0][0][1]
        re.append(graph[my_pre_layer_index][my_pre_inlayer_index])

        layer_index = my_pre_layer_index


    re.reverse()
    #print(re)
    return re




#--------------------------------------------
#API



def n_garm(sentence,garm=2):
    """

    :param sentence: 待分词的句子
    :param garm:
    :return: 分词结果 <list>
    """
    s_time = time.perf_counter()
    sentence =("B"+sentence+"E")
    graph = gen_graph(sentence=sentence)
    re = viterbi(graph)
    e_time = time.perf_counter()

    print("n-gram WP result", re)
    print("time",e_time-s_time)
    print("\n")

    return re



if __name__ == '__main__':
    load_grams()


    time1=time.perf_counter()
    n_garm(sentence="@所有人请大家尽快填写德育答辩时间统计问卷，时间需要尽快定下来～",garm=2)
    time2=time.perf_counter()
    print("taking "+str(time2-time1)+" time")


