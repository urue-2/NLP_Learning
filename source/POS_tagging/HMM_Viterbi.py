import json
import random
import math
import numpy as np
import time
#-----------------------------------
#configuration
word_class_number_for_this = 109


fp = "D:\\resource\\STUDY\\NLP\\2014_corpus.txt"
f1g = "corpus_resource/n_gram/2014_corpus_1gram.txt"
fpw = "corpus_resource/POS_source/pw_matrix.npy"
fcs = "corpus_resource/POS_source/word_class_static.txt"

pw_matrix = np.zeros([word_class_number_for_this,word_class_number_for_this])
gram1 = {}
all_class = {}
gram1_total_number  = 15439391



lpls_p1 = random.uniform(0, 1)
lpls_p2 = random.uniform(0, 1)

#------------------------------------------

def load_resource():
    """

    :return:
    """
    global pw_matrix , gram1 , all_class
    pw_matrix = np.load(fpw)
    gram1 = json.load(open(f1g,"r"))
    all_class = json.load(open(fcs,"r"))


def build_class_graph(word_list):
    """

    :param word_list: 分词后的结果 <list>
    :return: 词性构成的图 <list>
    """

    word_num = len(word_list)
    #print(word_list)
    #print(len(word_list))
    class_graph = [[] for i in range(word_num)]

    for (layer_index,word) in enumerate(word_list):
        #print(gram1.get(word))
        #print(gram1.get("中国"))
        class_graph[layer_index] += list(gram1.get(word,{}).keys())

    #print(class_graph)
    #print(len(class_graph))

    return class_graph

def cal_dis(word1,tag1,word2,tag2):
    """

    :param word1:
    :param tag1:
    :param word2:
    :param tag2:
    :return: 两个词以目前的词性的转移距离

    """

    ## w1/t1->w2/t2   -log(p(w2/t2))-log(p(tag1->tag2))
    word2_total_num = sum(list(gram1.get(word2,{}).values()))
    word2_tag2_num = gram1.get(word2).get(tag2,0)
    #lpls_p1*(lpls_p2*(f_w1_w2/f_word1) + 1-lpls_p2 )  +  (1-lpls_p1)*( (f_word1+1) /gram1_total_number)
    # lpls_p1*(lpls_p2*(word2_tag2_num/word2_total_num) + 1-lpls_p2 )  +  (1-lpls_p1)*( (word2_total_num) /gram1_total_number)
    p1 = lpls_p1*(lpls_p2*(word2_tag2_num/word2_total_num) + 1-lpls_p2 )  +  (1-lpls_p1)*( (word2_total_num) /gram1_total_number)

    all_class_list = list(all_class)
    try:
        tag1_index = all_class_list.index(tag1)
    except:
        tag1_index = -1
    try:
        tag2_index = all_class_list.index(tag2)
    except:
        tag2_index = -1

    if tag1_index==-1 or tag2_index==-1:
        tag1_to_tag2_num = 0
    else:
        tag1_to_tag2_num = pw_matrix[tag1_index][tag2_index]

    tag1_num = all_class.get(tag1,0)




    class_tran_total_number = 14155157
    p2 = lpls_p1*(lpls_p2*(tag1_to_tag2_num/tag1_num) + 1-lpls_p2 )  +  (1-lpls_p1)*( ( tag1_num +1) /class_tran_total_number)

    return -math.log(p1)-math.log(p2)







def pos_tagging_HMM_viterbi(wordlist):
    """

    :param wordlist:切分好的词 <list>
    :return: pos tagging result <list>
    """
    #print("in pos with len ",len(wordlist))
    s_time = time.perf_counter()
    load_resource()
    class_graph = build_class_graph(word_list=wordlist)
    #print("class graph",len(class_graph),class_graph)

    total_layer_number = len(class_graph)
    short_path = [[] for i in range(total_layer_number)]

    ## 向后计算部分

    for layer_index in range(total_layer_number):
        nodes_num = len(class_graph[layer_index])
        if layer_index == 0:
            #无前驱结点，初始化
            for in_layer_index in range(nodes_num):
                cur_word = wordlist[layer_index]
                cur_word_class = class_graph[layer_index][in_layer_index]
                t_dis = cal_dis(word1="BOS",tag1="start",word2=cur_word,tag2=cur_word_class)
                short_path[0].append([(in_layer_index,0),t_dis])





        else:
            # 计算层内每一个结点 我和前驱结点的距离，更新结点状态
            for in_layer_index in range(nodes_num):
                #print("in layer " , layer_index ,in_layer_index)
                cur_class = class_graph[layer_index][in_layer_index]
                cur_word = wordlist[layer_index]

                min_dis = math.inf
                min_in_layer_index = -1

                #print(cur_class,cur_word)
                ## (( class_graph l,il ),dis )
                for one_pre_reord in short_path[layer_index - 1]:
                    #print("one record",one_pre_reord)
                    my_pre_word = wordlist[layer_index - 1]
                    my_pre_in_layer_index = one_pre_reord[0][0]
                    my_pre_class = class_graph[layer_index-1][my_pre_in_layer_index]
                    #print("my pre",my_pre_word,my_pre_class,layer_index-1,my_pre_in_layer_index)

                    to_my_pre_dis = one_pre_reord[-1]

                    #print(my_pre_word,my_pre_class,cur_word,cur_class)

                    mdis_pre_me = to_my_pre_dis + cal_dis(word1=my_pre_word, tag1=my_pre_class, word2=cur_word, tag2=cur_class)

                    if mdis_pre_me < min_dis:
                        min_dis = mdis_pre_me

                        min_in_layer_index = my_pre_in_layer_index

                    if min_dis== math.inf :
                        min_in_layer_index = 0


                #每个结点 把自己的最近祖先的位置和距离放在最短路径中
                short_path[layer_index].append([(in_layer_index,min_in_layer_index),min_dis])
                #print( layer_index , short_path)

    # print(len(short_path))
    # for i in short_path:
    #     print(i)

    # 向前回溯过程
    short_path[-1].sort(key=lambda x: x[-1])
    cur_in_layer_index = short_path[-1][0][0][0]
    pre_in_layer_index = short_path[-1][0][0][1]
    re = []
    #print(short_path,len(short_path),total_layer_number)
    for i in range(total_layer_number)[::-1]:

        #print(wordlist[i],class_graph[i][cur_in_layer_index])
        re.append([wordlist[i],class_graph[i][cur_in_layer_index]])

        cur_in_layer_index = pre_in_layer_index
        #print(111,short_path[i-1][cur_in_layer_index][0][-1],"short_path[cur_in_layer_index][0][-1]")
        pre_in_layer_index = short_path[i-1][cur_in_layer_index][0][-1]


    re.reverse()

    e_time = time.perf_counter()
    print("POS result",re)
    print("time",e_time-s_time)
    print("\n")

    return re








if __name__ == '__main__':
    word_list = ['@', '所有', '人', '请', '大家', '尽快', '填写', '德育', '答辩', '时间', '统计', '问卷', '，时间', '需要', '尽快', '定', '下来', '～']
    re = pos_tagging_HMM_viterbi(wordlist=word_list)
